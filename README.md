# RDF Knowledge Graph Generator with RML and LLMs

A tool for generating knowledge graphs using RML mappings and LLM (Large Language Models) from semi-structured data.

---

## Project Structure

- **`main.py`** - The main script to run the pipeline.
- **`src/`** - Contains all supporting Python source files, including Python client (`query_llama.py`) for LLM queries invoked from within Java-based RML functions.
    - **`src/knowledge_graph`** - Contains all supporting Python source files for knowledge graph construction.
- **`requirements.txt`** - Lists all Python dependencies.
- **`resources/`** - Contains non-code files including:
    - **`evaluation/`** - Contains additional artefacts used for evaluation.
    - **`json/`** - Input JSON files for `drugs` and `interactions`.
    - **`knowledge-graphs/`** - Includes:
        - `ground-truth/`, `interactions/`, `rml/`, and `rml-llm/` subdirectories with:
            - RML mapping files
            - Generated RDF knowledge graphs
    - **`ontology/`** - RDFS ontology and SHACL constraints for drugs and interactions.
    - **`rml/`** - Contains RML function declarations and Java functions used by RML. Should include RMLMapper JAR file (see **Setup** step 7)
- **`java/`** - Contains Java function implementation/jar file used by RML mappings.
---

## Setup
1. Ensure `python3` is installed.
2. Clone the project.
3. Open a terminal window.
4. Create a virtual environment:
    ```bash
    python -m venv .venv
    ```
5. Activate the virtual environment:
    ```bash
    source .venv/bin/activate
    ```
6. Install dependencies (from root directory of the project):
    ```bash
    pip install -r requirements.txt
    ```
7. Download RMLMapper v7.3.3 jar from `https://github.com/RMLio/rmlmapper-java/releases/tag/v7.3.3` and add it to `resources/rml` directory (if not already included).
8. To deactivate the virtual environment:
    ```bash
    deactivate
    ```

Additionally:
- Ensure that `Java 17` is installed and available for RML processing.
- Ensure that `Ollama` is installed and the required LLM models are pulled.

In case the custom RML functions JAR file needs to be updated:
- Update the `RmlCustomFunctions.java` file in `java` directory.
- Run the following command to generate a new JAR file:
  ```bash
  javac -cp .:json-20250107.jar RmlCustomFunctions.java && jar cvf RmlCustomFunctions.jar RmlCustomFunctions.class
  ```
- Move the generated `RmlCustomFunctions.jar` to `resources/rml/` directory

---

## Running the Project

1. Open a terminal.
2. Activate the virtual environment:
    ```bash
    source .venv/bin/activate
    ```
3. Run the main script (from the root directory of the project) with `--help` flag to get a list of all options:
    ```bash
    python -m main --help
    ```
    ```plaintext
    options:
    -h, --help     show this help message and exit
    --asset ASSET  Select the asset to be generated (Mandatory).
                   Options: knowledge-graph, json
    --type TYPE    Select the generation type.
                   Options for "knowledge-graph": rml, rml-llm, all
    --itr ITR      Select the number of runs for knowledge graph and json. Default: 1
    --drugs DRUGS  Select the number of drugs to run rml-llm knowledge graph generation. Default: 20 (i.e. all drugs)
    --model MODEL  Select the LLM model. Any model pulled from Ollama will be supported.
    ```

4. Run the command by selecting relevant options.

   An example command to run *knowledge graph* construction using *rml-llm* (GenRML) for *3* iterations with *deepseek-r1:32b* model:
    ```bash
    python -m main --asset knowledge-graph --type rml-llm --model deepseek-r1:32b --itr 3
    ```
---