import dropbox
from common.dropbox_client import DropboxClient


def _process_entries(entries, file_list: list[str]):
    for entry in entries:
        if isinstance(entry, dropbox.files.FileMetadata):
            file_list.append(entry)


def _list_files(dropbox_client: DropboxClient, folder_path):
    files_response = dropbox_client.init_loading_files(folder_path)
    file_info = []

    _process_entries(files_response.entries, file_info)
    while files_response.has_more:
        files_response = dropbox_client.continue_loading_files(files_response.cursor)
        _process_entries(files_response.entries, file_info)

    return file_info


def _group_files_by_date(files) -> dict[str, list[dropbox.files.FileMetadata]]:
    grouped_files = {}
    for file in files:
        if isinstance(file, dropbox.files.FileMetadata):
            create_date = file.client_modified.strftime('%Y/%m')
            if create_date not in grouped_files:
                grouped_files[create_date] = []
            grouped_files[create_date].append(file)
    return grouped_files


def group_files(config):
    dbx_token = config['dropbox']['api_token']
    dbx = dropbox.Dropbox(dbx_token)
    dropbox_client = DropboxClient(dbx)

    target_directory = config['group']['directory']

    files_metadata = _list_files(dropbox_client, target_directory)
    grouped_files = _group_files_by_date(files_metadata)
    for date_group, files in grouped_files.items():
        job_id = dropbox_client.move_files_batch(dbx, files, f"{target_directory}/{date_group}")
        if job_id is None:
            break
        dropbox_client.check_job_status(dbx, job_id)