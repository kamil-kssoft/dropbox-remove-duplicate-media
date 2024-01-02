import json
import sys
import dropbox
from etaprogress.progress import ProgressBar


def _get_duplicate_filenames(input: dict[str, dict]) -> list[str]:
    result = []
    for _, record in input.items():
        result.extend(record['duplicates'])

    return result


def _move_files_to_trash(dbx, base_dir, trash_dir, filenames: list[str], bar: ProgressBar) -> None:
    counter = 0
    for filename in filenames:
        target_path = filename.replace(base_dir, trash_dir)
        dbx.files_move_v2(filename, target_path, autorename=True)
        counter += 1
        bar.numerator = counter
        print(bar, end='\r')
        sys.stdout.flush()


def remove_duplicates(config):
    with open('./data/resolved_metadata.json', encoding='utf-8') as json_file:
        data = json.load(json_file)

    duplicate_filenames = _get_duplicate_filenames(data)

    api_token = config['dropbox']['api_token']
    dbx = dropbox.Dropbox(api_token)
    base_dir = config['exclude']['base_dir']
    trash_dir = config['exclude']['temporary_trash_dir']
    bar = ProgressBar(len(duplicate_filenames), 60)
    print(bar, end='\r')
    sys.stdout.flush()
    _move_files_to_trash(dbx, base_dir, trash_dir, duplicate_filenames, bar)