import sys
import os

def check(args):
    if args[0].lower() != 'add':        
        return False

    folder_path = '.'
    if (len(args) > 1):
        folder_path = args[1]

    if os.path.isdir(folder_path):
        _run(folder_path)
        return True
    
    print(f"Error: The path '{folder_path}' is not a valid directory.")
    return False

def _run(folder_path):
    with open('paths.txt', 'a') as file:
        file.write(f"{os.path.abspath(folder_path)}\n")
    print(f"Added path: {os.path.abspath(folder_path)}")
