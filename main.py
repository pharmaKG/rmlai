import argparse
import logging

from pathlib import Path
from src import kg_generator

logging.basicConfig(
    format='%(asctime)s %(levelname)-8s %(message)s',
    level=logging.INFO,
    datefmt='%Y-%m-%d %H:%M:%S')


def main():
    parser = argparse.ArgumentParser(description="RDF Knowledge Graph Generator")
    parser.add_argument("--type", type=str, default="rml", help="Select generation type. Options are: rml, rml-llm, interactions, all. Default value rml.")

    args = parser.parse_args()

    if args.type == "rml-llm":
        generate_rml_llm_kg()
    elif args.type == "all":
        generate_rml_kg()
        generate_rml_llm_kg()
    else:
        generate_rml_kg()

def generate_rml_kg() -> None:
    logging.info("START: RML Knowledge Graph Generation")
    resources_dir = Path("resources")
    input_dir = resources_dir / "json" / "drugs"
    knowledge_graph_dir = resources_dir / "knowledge-graphs" / "rml"

    kg_generator.generate_kg(input_dir, knowledge_graph_dir, True)
    logging.info("END: RML Knowledge Graph Generation")

def generate_rml_llm_kg() -> None:
    logging.info("START: RML LLM Knowledge Graph Generation")
    resources_dir = Path("resources")
    input_dir = resources_dir / "json" / "drugs"
    knowledge_graph_dir = resources_dir / "knowledge-graphs" / "rml-llm"

    kg_generator.generate_kg(input_dir, knowledge_graph_dir, True)
    logging.info("END: RML LLM Knowledge Graph Generation")

if __name__=="__main__":
    main()