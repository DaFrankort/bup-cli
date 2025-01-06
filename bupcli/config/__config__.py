from pathlib import Path

def get_config_path():
    folder_name = ".bup-cli"
    config_dir = Path.home() / folder_name
    config_dir.mkdir(exist_ok=True)
    return config_dir

def get_hashes_path():
    config_path = get_config_path()
    folder_name = "hash"
    hash_dir = config_path / folder_name
    hash_dir.mkdir(exist_ok=True)
    return hash_dir