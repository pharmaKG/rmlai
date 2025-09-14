import argparse
import logging

from pathlib import Path

from src.knowledge_graph.json_generator import SimpleJsonGenerator, RagJsonGenerator
from src.knowledge_graph import knowledge_graph_generator

logging.basicConfig(
    format='%(asctime)s %(levelname)-8s %(message)s',
    level=logging.INFO,
    datefmt='%Y-%m-%d %H:%M:%S')

def main():
    parser = argparse.ArgumentParser(description="RDF Knowledge Graph Constructor", formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument("--asset", type=str, required=True, help="Select the asset to be generated (Mandatory). \nOptions: knowledge-graph, json")
    parser.add_argument("--type", type=str, help="Select the generation type. \nOptions for \"knowledge-graph\": rml, rml-llm, all")
    parser.add_argument("--itr", type=int, default=1, help="Select the number of runs for knowledge graph and json. Default: 1")
    parser.add_argument("--drugs", type=int, default=20, help="Select the number of drugs to run rml-llm knowledge graph generation. Default: 20 (i.e. all drugs)")
    parser.add_argument("--model", type=str, help="Select the LLM model. Any model pulled from Ollama will be supported.")

    args = parser.parse_args()

    if args.asset == "knowledge-graph" and args.type == "rml-llm" and args.model == "all":
        generate_rml_llm_kg("deepseek-r1:32b", args.itr, args.drugs)
        generate_rml_llm_kg("deepseek-r1:14b", args.itr, args.drugs)
        generate_rml_llm_kg("deepseek-r1:7b", args.itr, args.drugs)

    elif args.asset == "knowledge-graph" and args.type == "rml-llm" and args.model is not None:
        generate_rml_llm_kg(args.model, args.itr, args.drugs)

    elif args.asset == "knowledge-graph" and args.type == "all" and args.model is not None:
        generate_rml_kg(args.itr, args.drugs)
        generate_rml_llm_kg(args.model, args.itr, args.drugs)

    elif args.asset == "knowledge-graph" and args.type == "rml":
        generate_rml_kg(args.itr, args.drugs)

    elif args.asset == "json" and args.model is not None:
        generate_llm_json(args.model, args.itr)

    else:
        raise SystemExit("Command line argument doesn't combine.")

def generate_rml_kg(num_of_itr, num_of_drugs):
    logging.info("START: RML Knowledge Graph Generation")
    resources_dir = Path("resources")
    input_dir = resources_dir / "json" / "drugs"
    knowledge_graph_dir = resources_dir / "knowledge-graphs" / "rml"

    knowledge_graph_generator.generate_kg("none", input_dir, knowledge_graph_dir, num_of_itr, num_of_drugs, True)
    logging.info("END: RML Knowledge Graph Generation")

def generate_rml_llm_kg(model, num_of_itr, num_of_drugs):
    logging.info("START: RML LLM Knowledge Graph Generation with {}".format(model))
    resources_dir = Path("resources")
    input_dir = resources_dir / "json" / "drugs"
    knowledge_graph_dir = resources_dir / "knowledge-graphs" / "rml-llm"

    knowledge_graph_generator.generate_kg(model, input_dir, knowledge_graph_dir, num_of_itr, num_of_drugs, True)
    logging.info("END: RML LLM Knowledge Graph Generation with {}".format(model))

def generate_llm_json(model, num_of_itr):
    logging.info("START: LLM JSON Generation")
    resources_dir = Path("resources")

    logging.info("START: SIMPLE LLM JSON Generation")
    SimpleJsonGenerator(model=model, num_of_itr=num_of_itr, resources_dir=resources_dir).generate()
    logging.info("END: SIMPLE LLM JSON Generation")

    logging.info("START: RAG LLM JSON Generation")
    RagJsonGenerator(model=model, num_of_itr=num_of_itr, resources_dir=resources_dir).generate()
    logging.info("END: RAG LLM JSON Generation")

    logging.info("END: LLM JSON Generation")

if __name__=="__main__":
    main()