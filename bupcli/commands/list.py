from ..data import paths_manager as paths

def check(args):
    if args[0].lower() == 'list':        
        _run()

def _run():
    dirs = paths.read()

    if len(dirs) <= 0:
        print("No folders configured yet, add folders using `bup add <folder_path>`")
        return

    i = 1
    for dir in dirs:
        print(f"[{i}] - {dir}")
        i += 1