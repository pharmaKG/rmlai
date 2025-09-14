import logging
from pathlib import Path

from slugify import slugify

from src import queries, query_llama
from src.utils import find_file
from src.knowledge_graph.knowledge_graph_generator import get_time


class JsonGenerator:
    def __init__(self, model: str, input_dir: Path, output_dir: Path, prompt_dir: Path, num_of_itr: int):
        self.model = model
        self.input_dir = input_dir
        self.output_dir = output_dir
        self.prompt_dir = prompt_dir
        self.num_of_itr = num_of_itr

    def generate(self):
        for itr in range(self.num_of_itr):
            for query_id, query_data in queries.get().items():
                logging.info("Model: {} | ITR: {} | Generating JSON for: {}".format(self.model, itr, query_id))

                file = find_file(self.input_dir, (query_data["drug"] + ".json"))
                with open(file=file , mode="r") as input_file:
                    json = input_file.read()

                prompt_template_file = query_data["prompt-template"]
                with open(file=self.prompt_dir / prompt_template_file, mode="r") as template_file:
                    prompt = template_file.read().format(json=json, question=query_data["question"])

                output_file_name = slugify(self.model) + "_" + str(itr) + "_Q" + query_id + "_" + get_time()  + ".json"
                with open(file=self.output_dir / output_file_name, mode="w+") as output_file:
                    output_file.write(query_llama.query_general(prompt=prompt, model=self.model))

class RagJsonGenerator(JsonGenerator):
    def __init__(self, model: str, num_of_itr: int, resources_dir: Path):
        super().__init__(model=model,
                         input_dir=resources_dir / "json",
                         output_dir=resources_dir / Path("evaluation/json/rag/extracted"),
                         prompt_dir=resources_dir / Path("prompt/json/rag"),
                         num_of_itr=num_of_itr)

class SimpleJsonGenerator(JsonGenerator):
    def __init__(self, model: str, num_of_itr: int, resources_dir: Path):
        super().__init__(model=model,
                         input_dir=resources_dir / "json",
                         output_dir=resources_dir / Path("evaluation/json/simple/extracted"),
                         prompt_dir=resources_dir / Path("prompt/json/simple"),
                         num_of_itr=num_of_itr)