import os
import json

def _file_path():
    file_name = "dirs"
    folder_name = "data"
    os.makedirs(folder_name, exist_ok=True) # TODO Create init logic to create folder initially rather than every time
    return folder_name + "/" + file_name + ".json"

def add_path(relative_path):
    paths = read()
    abs_path = os.path.abspath(relative_path)

    if abs_path in paths:
        print(f"Path already exists: '{abs_path}'")
        return
    paths.append(abs_path)

    with open(_file_path(), 'w') as file:
        json.dump(paths, file, indent=4)
    print(f"Added path: '{abs_path}'")

def read():
    try:
        with open(_file_path(), 'r') as file:
            data = json.load(file)
    except FileNotFoundError:
        data = []
        with open(_file_path(), 'w') as file:
            json.dump(data, file, indent=4)

    return data