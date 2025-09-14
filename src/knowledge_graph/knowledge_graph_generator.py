import subprocess
import logging
import shutil
import tempfile

from typing import Tuple
import rdflib
from pathlib import Path
from slugify import slugify
import time
from src.utils import merge_files

##TODO: refactor
def generate_kg(model, input_dir, knowledge_graph_dir, num_of_itr, num_of_drugs, with_interaction) -> None:
    output_dir, rml_working_dir = prepare_rml_dir(model, knowledge_graph_dir)
    try:
        generate_individual_drug(model, input_dir, output_dir, rml_working_dir, num_of_itr, num_of_drugs)
        if with_interaction:
            generate_interaction_kg(model, output_dir, rml_working_dir)
            merge_graphs(knowledge_graph_dir, model, num_of_itr, output_dir)
    finally:
        try:
            logging.info("Cleaning {}".format(rml_working_dir))
            shutil.rmtree(rml_working_dir)
        except Exception as e:
            logging.warning("Cleanup failed for {}: {}".format(rml_working_dir, e))

def prepare_rml_dir(model, knowledge_graph_dir) -> Tuple[Path, Path]:
    rml_working_dir = Path(tempfile.mkdtemp(prefix="rmlai_")).absolute()
    output_dir = rml_working_dir / "output" / slugify(model)

    if not output_dir.exists():
        output_dir.mkdir(parents=True, exist_ok=True)

    shutil.copytree(Path("resources") / "rml", rml_working_dir, dirs_exist_ok=True)
    shutil.copy2(knowledge_graph_dir / "mapping.ttl", rml_working_dir)
    shutil.copy2(Path("src") / "query_llama.py", rml_working_dir)

    return output_dir, rml_working_dir

def generate_individual_drug(model, input_dir, output_dir, rml_working_dir, num_of_itr=1, num_of_drugs=20) -> None:
    for itr in range(num_of_itr):
        input_files = list(input_dir.iterdir())[:num_of_drugs]
        iterated_output_dir = output_dir / str(itr)
        iterated_output_dir.mkdir()
        generate_individual_graph(model, iterated_output_dir, rml_working_dir, input_files, itr)

def generate_individual_interaction(model, input_dir, output_dir, rml_working_dir) -> None:
    input_files = list(input_dir.iterdir())
    interactions_output_dir = output_dir / "interactions"
    interactions_output_dir.mkdir()
    generate_individual_graph(model, interactions_output_dir, rml_working_dir, input_files)

def generate_individual_graph(model, output_dir, rml_working_dir, input_files, itr=0):
    for input_file in input_files:
        if input_file.suffix != ".json":
            continue

        logging.info("START: MODEL - {}, ITR - {}, FILE - {}".format(model, str(itr), input_file))

        shutil.copy2(input_file, rml_working_dir)
        output_file_name = input_file.stem + "_" + slugify(model) + "_" + get_time() + ".nt"
        construct_graph(model=model,
                        drug_name=input_file.stem,
                        input_file=input_file.name,
                        output_file=output_dir / output_file_name,
                        mapping_folder=rml_working_dir)

        logging.info("END: {}".format(input_file))

def construct_graph(model, drug_name, input_file, output_file, mapping_folder) -> None:
    mapping_file = update_mapping(model, drug_name, input_file, mapping_folder)
    command = [
        "java", "-jar", "rmlmapper-7.3.3-r374-all.jar",
        "rmlmapper", "-f", "functions.ttl",
        "-m", str(mapping_file),
        "-o", str(output_file)
    ]
    logging.info("RML Mapping: {}".format(drug_name))
    run_command(command, mapping_folder)

def update_mapping(model, drug_name, input_file, mapping_folder) -> str:
    graph = rdflib.Graph()
    graph.parse(mapping_folder / "mapping.ttl", format="turtle")

    rml_source_update_query = get_rml_source_update_query(input_file)
    graph.update(rml_source_update_query)

    llm_model_update_query = get_llm_model_update_query(model)
    graph.update(llm_model_update_query)

    mapping_file = drug_name + ".rml.ttl"
    graph.serialize(mapping_folder / mapping_file, base="http://example/")

    return mapping_file

def get_rml_source_update_query(input_file):
    return ("""
        PREFIX rml: <http://semweb.mmlab.be/ns/rml#>
        PREFIX rr: <http://www.w3.org/ns/r2rml#>
        
        DELETE {{ ?logicalSource rml:source ?oldSource }}
        INSERT {{ ?logicalSource rml:source \"{}\" }}
        WHERE {{
            ?triplesMap a rr:TriplesMap .
            ?triplesMap rml:logicalSource ?logicalSource .
            ?logicalSource rml:source ?oldSource .
        }}
    """).format(input_file)


def get_llm_model_update_query(model) -> str:
    return ("""
        PREFIX rr: <http://www.w3.org/ns/r2rml#>
        
        DELETE {{ ?s rr:constant "LLM-MODEL-TEMPLATE" }}
        INSERT {{ ?s rr:constant \"{}\" }}
        WHERE {{
            ?s rr:constant "LLM-MODEL-TEMPLATE" .
        }}
    """).format(model)

def run_command(command, cwd=None) -> None:
    try:
        result = subprocess.run(
            command,
            cwd=cwd,
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            bufsize=1
        )
        if result.stdout:
            logging.info(result.stdout)
    except Exception as e:
        logging.error("COMMAND ERROR || Command: {} || Error: {}".format(str(command), str(e.stderr)))

def generate_interaction_kg(model, output_dir, rml_working_dir) -> None:
    logging.info("START: Interactions Knowledge Graph Generation")
    resources_dir = Path("resources")
    input_dir = resources_dir / "json" / "interactions"
    knowledge_graph_dir = resources_dir / "knowledge-graphs" / "interactions"

    shutil.copy2(knowledge_graph_dir / "mapping.ttl", rml_working_dir)

    generate_individual_interaction(model, input_dir, output_dir, rml_working_dir)
    logging.info("END: Interactions Knowledge Graph Generation")

def merge_graphs(knowledge_graph_dir, model, num_of_itr, output_dir):
    for itr in range(num_of_itr):
        graph_file_name = slugify(model) + "_" + get_time() + "_graph_" + str(itr) + ".nt"
        iterated_output_dir = output_dir / str(itr)
        interactions_output_dir = output_dir / "interactions"
        merge_files(knowledge_graph_dir / graph_file_name, iterated_output_dir, interactions_output_dir)

def get_time() -> str:
    return time.strftime("%Y%m%d-%H%M%S")