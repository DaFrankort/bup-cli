from ..managers import paths_manager as paths

def check_and_run(args):
    if args[0].lower() == 'list':        
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