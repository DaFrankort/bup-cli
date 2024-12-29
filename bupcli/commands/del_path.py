from ..managers import paths_manager as paths
from . import list_paths

def check_and_run(args):
    if args[0].lower() == 'del':        
        run()

def run():
    dirs = paths.read()

    if len(dirs) <= 0:
        print("No folders configured yet, add folders using `bup add <folder_path>`")
        return

    for i, dir in enumerate(dirs):
        print(f"[{i}] {dir}")

    print()
    try:
        user_choice = int(input("Enter number for the folder to remove from the backups-list: "))
        if user_choice < 0 or user_choice >= len(dirs):
            print("Invalid choice. Please select a valid folder number.")
            return
    except ValueError:
        print("Invalid input. Please enter a number.")
        return

    removed_folder = dirs[user_choice]
    del dirs[user_choice]    
    paths.write(dirs)
    print(f"Removed folder [{user_choice}]: {removed_folder}.")