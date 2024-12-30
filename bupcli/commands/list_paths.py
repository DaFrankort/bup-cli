from ..managers import paths_manager as paths
from ..managers import settings_manager as settings

def run(args):
    print_backup_dir()
    print()
    _print_dirs()
    
def print_backup_dir():
    backup_dir = settings.get_backup_directory()

    if backup_dir == None:
        print("No backup location set yet, set a directory using `bup set <folder_path>`")
    else:
        print(f"Backup location: {backup_dir}")

def _print_dirs():
    dirs = paths.read()
    if len(dirs) <= 0:
        print("No directories added yet, add directories using `bup add <folder_path>`")
        return

    if len(dirs) == 1:
        print(f"1 folder found:")
    else:
        print(f"{len(dirs)} folders found:")

    for dir in dirs:
        print(f"- {dir}")