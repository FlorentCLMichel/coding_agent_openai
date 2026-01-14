from functions.utils import *
from functions.config import MAX_CHARS 

def get_file_content(working_directory: str, file_path: str) -> str :
    target_file = os.path.join(working_directory, file_path)
    if not(os.path.isfile(target_file)):
        return f'ERROR: "{target_file}" is not a regular file'
    if not(path_is_parent(working_directory, target_file)):
        return f'ERROR: Cannot get the content of "{target_file}" as it is outside the permitted working directory {working_directory}'
    try:
        with open(target_file, "r", encoding="utf-8") as f:
            content = f.read(MAX_CHARS)
            if os.path.getsize(target_file) > MAX_CHARS:
                content += (
                    f'[...File "{file_path}" truncated at {MAX_CHARS} characters]'
                )
        return content
    except Exception as e:
        return f'ERROR reading file "{target_file}": {e}'
