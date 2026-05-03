from functions.utils import *

def move_file(working_directory, source_path, dest_path) -> str :
    rel_source_path = source_path
    rel_dest_path = dest_path
    source_path = os.path.join(working_directory, source_path)
    dest_path = os.path.join(working_directory, dest_path)
    if not(path_is_parent(working_directory, source_path)):
        return f'ERROR: Cannot access the source path "{rel_source_path}" as it is outside the permitted working directory'
    if not(path_is_parent(working_directory, dest_path)):
        return f'ERROR: Cannot access the destination path "{rel_dest_path}" as it is outside the permitted working directory'
    if not os.path.exists(dest_path):
        try:
            os.makedirs(os.path.dirname(dest_path), exist_ok=True)
        except Exception as e:
            return f"ERROR: creating directory: {e}"
    if not(os.path.exists(source_path)):
        return f'ERROR: "{rel_source_path}" does not exist'
    if os.path.isdir(source_path):
        return f'ERROR: "{rel_source_path}" is a directory, not a file'
    try:
        os.replace(source_path, dest_path)
        return f'Successfully moved "{rel_source_path}" to "{rel_dest_path}"'
    except Exception as e:
        return f"ERROR: moving the file file: {e}"
