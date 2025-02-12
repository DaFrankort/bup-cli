# __main__.py
import sys
from .commands import add_path
from .commands import list_paths
from .commands import del_path
from .commands import set_backup_dir
from .commands import run_backup

COMMAND_MAPPING = {
    'add': add_path.run,
    'a': add_path.run,
    'del': del_path.run,
    'd': del_path.run,
    'list': list_paths.run,
    'l': list_paths.run,
    'set': set_backup_dir.run,
    's': set_backup_dir.run,
    'run': run_backup.run,
    'r': run_backup.run
}

def main():
    args = sys.argv[1:]
    if len(args) == 0:
        print_command_mapping()
        return
    
    global COMMAND_MAPPING
    command = args[0].lower()
    action = COMMAND_MAPPING.get(command)
    if action:
        action(args)
    else:
        print(f"Unknown command: {command}")
        print_command_mapping()

def print_command_mapping():
    global COMMAND_MAPPING
    # TODO Create a command class to store the command synonyms, description and which function to run
    print("Available commands:")
    for command in COMMAND_MAPPING.keys():
        print(f"- {command}")

if __name__ == '__main__':
    main()