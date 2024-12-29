from ..managers import paths_manager as paths

def run(args):
    dirs = paths.read()

    if len(dirs) <= 0:
        print("No folders configured yet, add folders using `bup add <folder_path>`")
        return

    if len(dirs) == 1:
        print(f"1 folder found:")
    else:
        print(f"{len(dirs)} folders found:")

    for dir in dirs:
        print(f"- {dir}")