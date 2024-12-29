# __main__.py
import sys
from .commands import add_path
from .commands import list_paths
from .commands import del_path

def main():
    args = sys.argv[1:]
    if len(args) == 0:
        # TODO -> Print help command or version or something :-)
        print('No arguments given.')
        return

    command_mapping = {
        'add': add_path.run,
        'a': add_path.run,

        'del': del_path.run,
        'd': del_path.run,

        'list': list_paths.run,
        'l': list_paths.run,
    }
    
    command = args[0].lower()
    action = command_mapping.get(command)
    if action:
        action(args)
    else:
        print(f"Unknown command: {command}")
    
if __name__ == '__main__':
    main()