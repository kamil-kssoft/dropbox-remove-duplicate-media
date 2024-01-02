import json
import os


def _get_record_metadata(filenames: list[str], paths_to_remove: list[str], paths_to_maintain: list[str]):
    result = {
        'original': None,
        'duplicates': [],
    }
    for filename in filenames:
        if result['original'] is None \
            and _is_in_maintained_path(filename, paths_to_maintain) \
            and _is_not_in_removed_path(filename, paths_to_remove) \
            and not _contains_copy_suffix(filename):
            result['original'] = filename
        else:
            result['duplicates'].append(filename)

    return result if result['original'] else None


def _is_in_maintained_path(filename: str, paths_to_maintain: list[str]):
    path = os.path.dirname(filename)
    return path in paths_to_maintain


def _is_not_in_removed_path(filename: str, paths_to_remove: list[str]):
    path = os.path.dirname(filename)
    return path not in paths_to_remove


def _contains_copy_suffix(filename: str):
    return '(1)' in filename or '(2)' in filename or '(3)' in filename


def resolve_original_files(config):
    paths_to_maintain = config['directories']['to_maintain']
    paths_to_remove = config['directories']['to_remove']

    with open('./data/duplicates_by_hash.json', encoding='utf-8') as json_file:
        data = json.load(json_file)

    output = {hash: _get_record_metadata(filenames, paths_to_remove, paths_to_maintain) for hash, filenames in data.items()}
    output = {hash: record for hash, record in output.items() if record is not None}

    with open('./data/resolved_metadata.json', 'w', encoding='utf-8') as outfile:
        json.dump(output, outfile, indent=4)