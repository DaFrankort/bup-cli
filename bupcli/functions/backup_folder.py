import shutil
import os
import zipfile
import concurrent.futures

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

    num_dirs = len(dirs)
    dst_path = _prepare_and_get_dst_path(dst_parent)
    num_workers = _get_optimal_workers(num_dirs)

    if num_dirs == 1:
        print(f"Starting BUP for 1 directory using {num_workers} workers:")
    else:
        print(f"Starting BUP for {num_dirs} directories using {num_workers} workers:")

    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = [executor.submit(_backup, Path(src), dst_path) for src in dirs]
        for future in concurrent.futures.as_completed(futures):
            try:
                future.result()
            except Exception as e:
                print(f"Error during backup: {e}")

    print("BUP completed.")

def _get_optimal_workers(num_dirs):
    cpu_cores = os.cpu_count()

    # If there are more directories than CPU cores, use the number of directories
    # Otherwise, use a fraction of CPU cores or the number of cores
    if num_dirs > cpu_cores:
        return min(cpu_cores, num_dirs)
    else:
        return cpu_cores

def _prepare_and_get_dst_path(dst_parent):
    folder_name = "Backups"
    dst_path = Path(dst_parent) / folder_name

    if dst_path.exists():
        old_folder_name = f"{folder_name}_Old"
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
    zip_name =  str(src_path).replace("\\", "_").replace("/", "_").replace("__", "_")
    zip_name = _cleanup_path_string(zip_name)
    filename = f"{zip_name}.zip"
    dst_zip_path  = dst_path / filename

    try:
        with zipfile.ZipFile(dst_zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
            total_files = sum([len(files) for r, d, files in os.walk(src_path)])
            with tqdm(total=total_files, desc=f"Zipping '{filename}'") as pbar:
                for dirpath, dirnames, filenames in os.walk(src_path):
                    for filename in filenames:
                        file_path = Path(dirpath) / filename
                        arcname = file_path.relative_to(src_path)
                        zipf.write(file_path, arcname=arcname)
                        pbar.update(1)
    except Exception as e:
        print(f"Error during backup: {e}")

def _cleanup_path_string(path_str):
    symbols = ["\\", "/", ":", " ", "."]
    for symbol in symbols:
        path_str = path_str.replace(symbol, "")
    
    return path_str