import json
from pathlib import Path

def read_file_as_json(file) -> dict:
    with open(file=file, mode="r") as f:
        return json.load(f)

def read_as_json(json_obj) -> dict:
    return json.loads(json_obj)

def save_json_to_file(file: Path, json_obj) -> None:
    file.parent.mkdir(parents=True, exist_ok=True)
    with open(file=file, mode="w+") as json_file:
        json.dump(json_obj, json_file, indent=4)

def find_file(parent_folder, target_file):
    parent_path = Path(parent_folder)
    for file in parent_path.rglob(target_file):
        return file
    return None

def merge_files(output_path, *sources):
    with open(output_path, "w") as outfile:
        for source in sources:
            print("Merging Start: {}".format(source))
            for file in source.iterdir():
                with open(file, "r") as infile:
                    outfile.write(infile.read())

    print("Merging End!")