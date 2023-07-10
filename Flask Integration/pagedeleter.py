import os
import shutil

def deletepage(folder):
    for filename in os.listdir(folder):
        file_path = os.path.join(folder, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            return ('Failed to delete %s. Reason: %s' % (file_path, e))
    return "File from {i} deleted successfully".format(i=folder)

import os

def delete_files(files):
    """
    Delete one or multiple files specified by the file paths.

    Parameters:
    - files: A single file path or a list of file paths to be deleted.

    Returns:
    None
    """
    if isinstance(files, str):
        files = [files]  # Convert single file path to a list for consistent handling

    for file in files:
        try:
            os.remove(file)
            print(f"File '{file}' deleted successfully.")
        except OSError as e:
            if e.errno == 2:
                print(f"File '{file}' does not exist.")
            else:
                print(f"Failed to delete file '{file}'. Error: {str(e)}")
        except Exception as e:
            print(f"An error occurred while deleting file '{file}'. Error: {str(e)}")
            