import os
import json
from . import settings_manager as settings
from .  import __config__ as config

def _file_path():
    file_name = "dirs"
    folder_path = config.get_config_path()
    return str(folder_path / f"{file_name}.json")

def add_path(relative_path):
    paths = read()
    abs_path = os.path.abspath(relative_path)

    if abs_path in paths:
        print(f"Path already exists: '{abs_path}'")
        return

    backup_dir = settings.get_backup_directory()
    if backup_dir == abs_path:
        print(f"Can't add '{abs_path}' to the directory list, it is already set as backup-directory.")
        print(f"If you are certain you want to back this folder up, set a different backup-directory first using `bup set <folder_path>`.")
        return
    
    paths.append(abs_path)
    paths.sort()
    
    with open(_file_path(), 'w') as file:
        json.dump(paths, file, indent=4)
    print(f"Added path: '{abs_path}'")

def write(data):
    with open(_file_path(), 'w') as file:
        json.dump(data, file, indent=4)

def read():
    try:
        with open(_file_path(), 'r') as file:
            data = json.load(file)
    except FileNotFoundError:
        data = []
        with open(_file_path(), 'w') as file:
            json.dump(data, file, indent=4)

    return data