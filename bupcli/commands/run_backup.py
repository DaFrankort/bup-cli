from ..functions import backup_folder as backup

def run(args):
    print("Starting backup process...")
    print()
    backup.backup_all()