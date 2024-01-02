import dropbox
import json
from common.dropbox_client import DropboxClient


def _process_entries(entries, file_list: list[str]):
    for entry in entries:
        if isinstance(entry, dropbox.files.FileMetadata):
            file_list.append({'path': entry.path_lower, 'name': entry.name, 'size': entry.size, 'hash': entry.content_hash})


def _list_files(dropbox_client: DropboxClient, folder_path):
    files_response = dropbox_client.init_loading_files(folder_path, recursive=True)
    file_info = []

    _process_entries(files_response.entries, file_info)
    while files_response.has_more:
        files_response = dropbox_client.continue_loading_files(files_response.cursor)
        _process_entries(files_response.entries, file_info)

    return file_info


def _get_duplicates(file_info):
    duplicates_by_hash = {}
    for file in file_info:
        if file['hash'] in duplicates_by_hash:
            duplicates_by_hash[file['hash']].append(file['path'])
        else:
            duplicates_by_hash[file['hash']] = [file['path']]

    return {name: paths for name, paths in duplicates_by_hash.items() if len(paths) > 1}


def find_duplicates(config):
    api_token = config['dropbox']['api_token']
    directories_to_find = config['duplicates']['directories_to_find']

    dbx = dropbox.Dropbox(api_token)
    dropbox_client = DropboxClient(dbx)

    file_info = []
    for folder in directories_to_find:
        file_info.extend(_list_files(dropbox_client, folder))

    duplicates_by_hash = _get_duplicates(file_info)
    with open('./data/duplicates_by_hash.json', 'w') as f:
        json.dump(duplicates_by_hash, f, indent=4)

    print('Found duplicates have been saved to JSON files')