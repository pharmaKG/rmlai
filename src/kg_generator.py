import subprocess
import logging
import shutil
import tempfile

from typing import Tuple
from rdflib import Graph
from pathlib import Path
from . import rdf_processor

def generate_kg(input_dir, knowledge_graph_dir, with_interaction) -> None:
    output_dir, rml_working_dir = prepare_rml_dir(knowledge_graph_dir)
    try:
        generate(input_dir, output_dir, rml_working_dir)
        if with_interaction:
            generate_interaction_kg(rml_working_dir)
            rdf_processor.merge(knowledge_graph_dir / "graph.nt", output_dir)
    finally:
        try:
            shutil.rmtree(rml_working_dir)
        except Exception as e:
            logging.warning("Cleanup failed for {}: {}".format(rml_working_dir, e))

def prepare_rml_dir(knowledge_graph_dir) -> Tuple[Path, Path]:
    rml_working_dir = Path(tempfile.mkdtemp(prefix="rmlai_")).absolute()
    output_dir = rml_working_dir / "output"

    if not output_dir.exists():
        output_dir.mkdir(parents=True, exist_ok=True)

    shutil.copytree(Path("resources") / "rml", rml_working_dir, dirs_exist_ok=True)
    shutil.copy2(knowledge_graph_dir/ "mapping.ttl", rml_working_dir)
    shutil.copy2(Path("src") / "query_llama.py", rml_working_dir)

    return output_dir, rml_working_dir

def generate(input_dir, output_dir, rml_working_dir) -> None:
    for input_file in input_dir.iterdir():
        if input_file.suffix != ".json":
            continue

        logging.info("START: {}".format(input_file))

        shutil.copy2(input_file, rml_working_dir)
        output_file_name = input_file.stem + ".nt"
        construct(drug_name=input_file.stem,
                  input_file=input_file.name,
                  source_mapping=rml_working_dir / "mapping.ttl",
                  output_file=output_dir / output_file_name,
                  mapping_folder=rml_working_dir)

        logging.info("END: {}".format(input_file))

def construct(drug_name, input_file, source_mapping, output_file, mapping_folder) -> None:
    kg = Graph()
    kg.parse(source_mapping, format="turtle")

    # SPARQL UPDATE query to update rml:source
    mapping_file = update_rml_source(drug_name, input_file, mapping_folder, kg)

    command = [
        "java", "-jar", "rmlmapper-7.3.3-r374-all.jar",
        "rmlmapper", "-f", "functions.ttl",
        "-m", str(mapping_file),
        "-o", str(output_file)
    ]
    logging.info("RML Mapping: {}".format(drug_name))
    run_command(command, mapping_folder)

def update_rml_source(drug_name, input_file, mapping_folder, kg) -> str:
    update_query = ("""
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
    kg.update(update_query)

    mapping_file = drug_name + ".rml.ttl"
    kg.serialize(mapping_folder / mapping_file, base="http://example/")

    return mapping_file

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

def generate_interaction_kg(rml_working_dir) -> None:
    logging.info("START: Interactions Knowledge Graph Generation")
    resources_dir = Path("resources")
    input_dir = resources_dir / "json" / "interactions"
    knowledge_graph_dir = resources_dir / "knowledge-graphs" / "interactions"

    shutil.copy2(knowledge_graph_dir / "mapping.ttl", rml_working_dir)

    generate(input_dir, rml_working_dir / "output", rml_working_dir)
    logging.info("END: Interactions Knowledge Graph Generation")