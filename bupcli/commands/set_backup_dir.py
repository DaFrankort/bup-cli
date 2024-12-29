import os
from ..managers import settings_manager as settings

def run(args):
    relative_path = '.'
    if (len(args) > 1):
        relative_path = args[1]

    if not os.path.isdir(relative_path):
        print(f"Error: The path '{relative_path}' is not a valid directory.")
        return False

    settings.set_backup_directory(relative_path)
    return True