from functions.utils import *

def move_file(working_directory, source_path, dest_path) -> str :
    source_path = os.path.join(working_directory, source_path)
    dest_path = os.path.join(working_directory, dest_path)
    if not(path_is_parent(working_directory, source_path)):
        return f'ERROR: Cannot access the source path "{source_path}" as it is outside the permitted working directory {working_directory}'
    if not(path_is_parent(working_directory, dest_path)):
        return f'ERROR: Cannot access the destination path "{dest_path}" as it is outside the permitted working directory {working_directory}'
    if not os.path.exists(dest_path):
        try:
            os.makedirs(os.path.dirname(dest_path), exist_ok=True)
        except Exception as e:
            return f"ERROR: creating directory: {e}"
    if not(os.path.exists(source_path)):
        return f'ERROR: "{source_path}" does not exist'
    if os.path.isdir(source_path):
        return f'ERROR: "{source_path}" is a directory, not a file'
    try:
        os.replace(source_path, dest_path)
        return f'Successfully moved "{source_path}" to "{dest_path}"'
    except Exception as e:
        return f"ERROR: moving the file file: {e}"
