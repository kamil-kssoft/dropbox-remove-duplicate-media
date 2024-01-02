import dropbox
from common.dropbox_client import DropboxClient


def move_files(config):
    dropbox_token = config['dropbox']['api_token']
    dbx = dropbox.Dropbox(dropbox_token)
    dropbox_client = DropboxClient(dbx)

    for source_dir in config['store']['source_dirs']:
        while True:
            job_id = dropbox_client.move_files_batch(dbx, source_dir, config['store']['target_dir'])
            if job_id is None:
                break
            dropbox_client.check_job_status(dbx, job_id)