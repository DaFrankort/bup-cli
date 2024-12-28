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

    i = 0
    for dir in dirs:
        print(f"[{i}] - {dir}")
        i += 1

    print()
    user_choice = int(input("Enter number for the folder to remove from the backups-list: "))
    # TODO: Validate if selection is actually an INT

    dirs.remove(user_choice)
    paths.write(dirs)
    print(f"Removed folder {user_choice}: {dirs[user_choice]}.")
