import os
from ..managers import paths_manager as paths

def check_and_run(args):
    if args[0].lower() != 'add':        
        return False

    relative_path = '.'
    if (len(args) > 1):
        relative_path = args[1]

    if not os.path.isdir(relative_path):
        print(f"Error: The path '{relative_path}' is not a valid directory.")
        return False

    _run(relative_path)
    return True

def _run(relative_path):
    paths.add_path(relative_path)


