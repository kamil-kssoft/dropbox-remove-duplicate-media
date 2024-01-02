import json
import os


def _extract_unique_paths(input_dict):
    unique_paths = set()
    for file_paths in input_dict.values():
        for path in file_paths:
            directory_path = os.path.dirname(path)
            unique_paths.add(directory_path)
    return list(unique_paths)


def extract_unique_paths():
    with open('./data/duplicates_by_hash.json', encoding='utf-8') as json_file:
        data = json.load(json_file)

    values = sorted(_extract_unique_paths(data))

    with open('./data/unique_paths.json', 'w', encoding='utf-8') as outfile:
        json.dump(values, outfile, indent=4)