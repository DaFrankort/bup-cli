import os
import json

def _file_path():
    file_name = "settings"
    folder_name = "data"
    os.makedirs(folder_name, exist_ok=True) # TODO Create init logic to create folder initially rather than every time
    return folder_name + "/" + file_name + ".json"

def set_backup_directory(relative_path):
    data = read()
    abs_path = os.path.abspath(relative_path)

    if 'backups_dir' not in data:
        data['backups_dir'] = None
    
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