from functions.utils import *

def write_file(working_directory, file_path, content) -> str :
    file_path = os.path.join(working_directory, file_path)
    if not(path_is_parent(working_directory, file_path)):
        return f'ERROR: Cannot write "{file_path}" as it is outside the permitted working directory {working_directory}'
    if not os.path.exists(file_path):
        try:
            os.makedirs(os.path.dirname(file_path), exist_ok=True)
        except Exception as e:
            return f"ERROR: creating directory: {e}"
    if os.path.exists(file_path) and os.path.isdir(file_path):
        return f'ERROR: "{file_path}" is a directory, not a file'
    try:
        with open(file_path, 'w') as f:
            f.write(content)
        return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
    except Exception as e:
        return f"ERROR: writing to file: {e}"
