from pathlib import Path

def get_config_path():
    folder_name = ".bup-cli"
    config_dir = Path.home() / folder_name
    config_dir.mkdir(exist_ok=True)
    return config_dir