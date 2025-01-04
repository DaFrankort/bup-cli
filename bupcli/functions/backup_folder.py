import shutil
import os
import hashlib
import base64

from pathlib import Path
from tqdm import tqdm
from  ..config import settings_manager as settings
from  ..config import paths_manager as paths

def backup_all():
    dst_parent = settings.get_backup_directory()
    if dst_parent == None:
        print("No backup location set yet, set a directory using `bup set <folder_path>`")
        return

    dirs = paths.read()
    if len(dirs) == 0:
        print("No directories added yet, add directories using `bup add <folder_path>`")
        return

    dst_path = _prepare_and_get_dst_path(dst_parent)

    if len(dirs) == 1:
        print(f"Starting bup for 1 directory:")
    else:
        print(f"Starting bup for {len(dirs)} directories:")


    for src in dirs:
        src_path = Path(src)

        sub_folder = _cleanup_path_string(src_path.parts[0])
        sub_dir = dst_path / sub_folder.capitalize()
        sub_dir.mkdir(parents=True, exist_ok=True)

        _backup(src_path, sub_dir)

    print("bup complete.")

def _prepare_and_get_dst_path(dst_parent):
    folder_name = "bup_backups"
    dst_path = Path(dst_parent) / folder_name

    if dst_path.exists():
        old_folder_name = f"{folder_name}_old"
        old_dst_path = Path(dst_parent) / old_folder_name
    
        if old_dst_path.exists():
            try:
                shutil.rmtree(old_dst_path)
            except OSError as e:
                print(f"Error deleting old backup folder: {e.strerror}")
        
        try:
            shutil.move(str(dst_path), str(old_dst_path))
        except Exception as e:
            print(f"Error renaming folder: {e}")
    
    dst_path.mkdir(parents=True, exist_ok=True)
    return dst_path

def _backup(src_path, dst_path):
    folder_name = src_path.parts[-1]
    path_hash = _generate_base64_key_from_path(src_path)

    dst_path_folder = dst_path / f"{folder_name}_{path_hash}"

    try:
        dst_path_folder.mkdir(parents=True, exist_ok=True)
        
        total_files = sum([len(files) for r, d, files in os.walk(src_path)])
        with tqdm(total=total_files, desc=f"Copying '{str(src_path)}'") as pbar:
            shutil.copytree(src_path, dst_path_folder, dirs_exist_ok=True, 
                            ignore=shutil.ignore_patterns('.git', '__pycache__'), 
                            copy_function=lambda src, dst: _copy_and_update_progress(src, dst, pbar))

    except Exception as e:
        print(f"Error during backup: {e}")

def _copy_and_update_progress(src, dst, pbar):
    """Helper function to update progress bar during file copy."""
    shutil.copy2(src, dst)
    pbar.update(1)

def _cleanup_path_string(path_str):
    symbols = ["\\", "/", ":", " ", "."]
    for symbol in symbols:
        path_str = path_str.replace(symbol, "")
    
    return path_str

def _generate_base64_key_from_path(src_path, length=8):
    """Generate a Base64-encoded unique key from the full path using a hash."""
    try:
        path_str = _cleanup_path_string(str(src_path))
        hash_object = hashlib.md5(path_str.encode())
        hash_bytes = hash_object.digest()
        base64_encoded = base64.urlsafe_b64encode(hash_bytes).decode('utf-8')
        return base64_encoded[:length]
    except Exception as e:
        print(f"Error generating Base64 key for path '{src_path}': {e}")
        return "unknown"  # Return a default key if there's an error