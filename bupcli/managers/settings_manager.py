import os
import json
from . import paths_manager as paths
from .  import config_handler as config

def _file_path():
    file_name = "settings"
    folder_path = config.get_config_path()
    return str(folder_path / f"{file_name}.json")

def set_backup_directory(relative_path):
    data = read()
    abs_path = os.path.abspath(relative_path)

    if 'backups_dir' not in data:
        data['backups_dir'] = None

    dirs = paths.read()
    for path in dirs:
        if path == abs_path:
            print(f"Can't set '{abs_path}' as backup directory, this directory is in the directory-list.")
            print(f"Remove this directory first using `bup del <folder_path>`.")
            return
    
    data['backups_dir'] = abs_path
    with open(_file_path(), 'w') as file:
        json.dump(data, file, indent=4)
    print(f"Set backup directory to: '{abs_path}'")

def get_backup_directory():
    data = read()
    if 'backups_dir' not in data:
        return None
    
    return data['backups_dir']

def read():
    try:
        with open(_file_path(), 'r') as file:
            data = json.load(file)
    except FileNotFoundError:
        data = {}
        with open(_file_path(), 'w') as file:
            json.dump(data, file, indent=4)

    return data