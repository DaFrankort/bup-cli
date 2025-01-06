import shutil
import os
import zipfile
import concurrent.futures
import hashlib

from pathlib import Path
from tqdm import tqdm
from ..config import settings_manager as settings
from ..config import paths_manager as paths
from ..config import __config__ as config

def backup_all():
    dst_parent = settings.get_backup_directory()
    if dst_parent == None:
        print("No backup location set yet, set a directory using `bup set <folder_path>`")
        return

    dirs = paths.read()
    if len(dirs) == 0:
        print("No directories added yet, add directories using `bup add <folder_path>`")
        return

    print("Checking directories...")
    valid_dirs = []
    for path in dirs:
        print(f"* '{path}'")
        path = Path(path)
        if not os.path.isdir(path):
            print(f"   !!! Does not exist !!!")
        elif not _folder_has_changes(path):
            print(f"   - No changes since last backup.")
        else:
            print("   - Changes detected.")
            valid_dirs.append(path)

    num_dirs = len(valid_dirs)
    dst_path = _prepare_and_get_dst_path(dst_parent)
    num_workers = _get_optimal_workers(num_dirs)

    if num_dirs == 0:
        print("No files to back-up.")
        return
    
    print()
    if num_dirs == 1:
        print(f"Starting Backup for 1 directory using {num_workers} workers:")
    else:
        print(f"Starting Backup for {num_dirs} directories using {num_workers} workers:")

    with concurrent.futures.ThreadPoolExecutor(max_workers=num_workers) as executor:
        futures = [executor.submit(_backup, Path(src), dst_path) for src in valid_dirs]
        for future in concurrent.futures.as_completed(futures):
            try:
                future.result()
            except Exception as e:
                print(f"Error during backup: {e}")

    print()
    print("Backups completed.")

def _get_optimal_workers(num_dirs):
    cpu_cores = os.cpu_count()
    return min(num_dirs, cpu_cores)

def _prepare_and_get_dst_path(dst_parent):
    folder_name = "Backups"
    dst_path = Path(dst_parent) / folder_name
    
    dst_path.mkdir(parents=True, exist_ok=True)
    return dst_path

def _backup(src_path, dst_path):
    filename = _convert_to_filename(src_path, "zip")
    dst_zip_path  = dst_path / filename
    if dst_zip_path.exists():
        try:
            os.remove(dst_zip_path)
        except Exception as e:
            print(f"Error removing existing zip file '{dst_zip_path}': {e}")
            return

    try:
        total_files = sum(len(files) for _, _, files in os.walk(src_path))
        with zipfile.ZipFile(dst_zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
            with tqdm(total=total_files, desc=f"* Zipping '{filename}'") as pbar:
                for dirpath, dirnames, filenames in os.walk(src_path):
                    for filename in filenames:
                        file_path = Path(dirpath) / filename
                        arcname = file_path.relative_to(src_path)
                        zipf.write(file_path, arcname=arcname)
                        pbar.update(1)
    except Exception as e:
        print(f"Error during backup: {e}")

def _folder_has_changes(path):
    """
    Check if a folder has changed based on the SHA256 hash of its contents.

    Args:
        path (str or Path): Path to the folder to check.

    Returns:
        bool: True if the folder has changed, False otherwise.
    """

    hash_sha256 = hashlib.sha256()
    for dir_path, _, filenames in sorted(os.walk(path)):
        dir_path = Path(dir_path)

        for filename in sorted(filenames):
            file_path = dir_path / filename

            try:
                if not file_path.exists():
                    continue

                # Add relative path and file size to the hash
                rel_path = str(file_path.relative_to(path))
                hash_sha256.update(rel_path.encode())
                hash_sha256.update(str(file_path.stat().st_size).encode())

                # Add file content to the hash
                # with open(file_path, 'rb') as f:
                #     while chunk := f.read(8192):
                #         hash_sha256.update(chunk)

            except FileNotFoundError:
                print(f"File not found: {file_path}. Skipping...")
            except PermissionError:
                print(f"Permission denied: {file_path}. Skipping...")
            except Exception as e:
                print(f"Error processing file {file_path}: {e}. Skipping...")

    hash_value = hash_sha256.hexdigest()

    filename = _convert_to_filename(path, "txt")
    hash_path = config.get_hashes_path() / filename

    if hash_path.exists():
        with open(hash_path, 'r') as f:
            stored_hash = f.read().strip()
        if stored_hash == hash_value:
            return False

    with open(hash_path, 'w') as f:
        f.write(hash_value)
    return True

def _convert_to_filename(path, filetype):
    if path == None:
        print("backup_folder.py => No path given, cannot convert.")
        return
    if filetype == None:
        print("backup_folder.py => No filetype given, cannot convert.")
        return

    filename = str(path)
    filename = filename.replace("\\", "_").replace("/", "_").replace("__", "_")
    filename = _cleanup_path_string(filename)

    filetype = filetype.replace(".","")

    return f"{filename}.{filetype}"

def _cleanup_path_string(path_str):
    symbols = ["\\", "/", ":", " ", "."]
    for symbol in symbols:
        path_str = path_str.replace(symbol, "")
    
    return path_str