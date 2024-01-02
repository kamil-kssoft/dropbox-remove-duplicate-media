import sys
import time
import dropbox

class DropboxClient:

    def __init__(self, dbx):
        self.dbx = dbx


    def init_loading_files(self, folder_path, recursive=False):
        try:
            return self.dbx.files_list_folder(folder_path, recursive=recursive)
        except dropbox.exceptions.ApiError as err:
            print(f'Error during listing files: {err}')
            return None
        except Exception as err:
            print(f'Unknown error: {err}')
            return None


    def continue_loading_files(self, cursor):
        try:
            return self.dbx.files_list_folder_continue(cursor)
        except dropbox.exceptions.ApiError as err:
            print(f'Error during listing files: {err}')
            return None
        except Exception as err:
            print(f'Unknown error: {err}')
            return None


    def move_files_batch(self, dbx, source_dir, target_dir):
        files_to_move = self.dbx.files_list_folder(source_dir).entries

        # Prepare the entries for move_batch
        entries = [dropbox.files.RelocationPath(file.path_lower, target_dir + '/' + file.name)
                for file in files_to_move if isinstance(file, dropbox.files.FileMetadata)]
        if len(entries) == 0:
            print("There are no files in the source directory. Aborting.")
            return None

        # Perform the batch move
        result = dbx.files_move_batch(entries, autorename=True)
        job_id = result.get_async_job_id()

        print(f"Moving files to dir {target_dir}, files count: {len(entries)}, job ID: {job_id}")

        return job_id


    def check_job_status(self, dbx, job_id):
        print("Checking job status: ", end='')
        sys.stdout.flush()
        while True:
            status = dbx.files_move_batch_check(job_id)
            if status.is_complete() or status.is_failed():
                break
            print('#', end='')
            sys.stdout.flush()
            time.sleep(10)

        print('')
        msg = "Batch move completed successfully." if status.is_complete() else "Batch move failed."
        print(msg)