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