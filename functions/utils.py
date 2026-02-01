import os

HISTORY_FILE = ".chat.history"

def reprint(message: str):
    with open(HISTORY_FILE, "a") as history_file:
        history_file.write(message + '\n')
    print(message)

def path_is_parent(parent_path: str, child_path: str) -> bool :
    parent_path = os.path.abspath(parent_path)
    child_path = os.path.abspath(child_path)
    return os.path.commonpath([parent_path]) == os.path.commonpath([parent_path, child_path])
