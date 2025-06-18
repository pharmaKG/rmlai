# Knowledge Graph Generation with RML and LLM

A tool for generating knowledge graphs using RML mappings and LLM (Large Language Model) from semi-structured data.

---

## Project Structure

- **`main.py`** - The main script to run the pipeline.
- **`src/`** - Contains all supporting Python source files, including Python client (`query_llama.py`) for LLM queries invoked from within Java-based RML functions.
- **`requirements.txt`** - Lists all Python dependencies.
- **`resources/`** - Contains non-code files including:
  - **`json/`** - Input JSON files for `drugs` and `interactions`.
  - **`knowledge-graphs/`** - Includes:
    - `ground-truth/`, `interactions/`, `rml/`, and `rml-llm/` subfolders with:
      - RML mapping files
      - Generated RDF knowledge graphs
  - **`ontology/`** - RDFS ontology and SHACL constraints for drugs and interactions.
  - **`queries/`** - SPARQL queries used for evaluation.
  - **`rml/`** - Contains:
    - RML JAR file
    - RML function declarations
    - Java functions used by RML
---

## Setup

1. Open a terminal window.
2. Create a virtual environment:
   ```bash
   python -m venv .venv
   ```
3. Activate the virtual environment:
   ```bash
   source .venv/bin/activate
   ```
4. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
5. To deactivate the virtual environment:
   ```bash
   deactivate
   ```

Additionally, ensure Java is installed and available in your system for RML processing.

---

## Running the Project

1. Open a terminal.
2. Activate the virtual environment:
   ```bash
   source .venv/bin/activate
   ```
3. Run the main script:
   ```bash
   python -m main.py --type ${type}
   ```
   Replace `${type}` with one of the following options:
  - `rml`: Generate the knowledge graph using RML only.
  - `rml-llm`: Generate the knowledge graph using both RML and LLM.
  - `all`: Generate both types of knowledge graphs.
---