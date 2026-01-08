from functions.utils import *

def create_dir(working_directory, dir_path) -> str :
    dir_path = os.path.join(working_directory, dir_path)
    if not(path_is_parent(working_directory, dir_path)):
        return f'ERROR: Cannot write "{dir_path}" as it is outside the permitted working directory {working_directory}'
    if not os.path.exists(dir_path):
        try:
            os.makedirs(dir_path, exist_ok=True)
            return f'Successfully created "{dir_path}"'
        except Exception as e:
            return f"ERROR: creating directory: {e}"
