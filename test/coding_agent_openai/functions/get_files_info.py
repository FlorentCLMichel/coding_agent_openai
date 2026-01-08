from functions.utils import *

def get_files_info(working_directory: str, directory: str = ".") -> str :
    target_dir = os.path.join(working_directory, directory)
    if not(os.path.isdir(target_dir)):
        return f'ERROR: "{target_dir}" is not a directory'
    if not(path_is_parent(working_directory, target_dir)):
        return f'ERROR: Cannot list "{target_dir}" as it is outside the permitted working directory {working_directory}'
    try:
        files_info = []
        for filename in os.listdir(target_dir):
            filepath = os.path.join(target_dir, filename)
            file_size = 0
            is_dir = os.path.isdir(filepath)
            file_size = os.path.getsize(filepath)
            files_info.append(
                f"{filename} — size: {file_size} bytes, directory: {is_dir}"
            )
        return "\n".join(files_info)
    except Exception as e:
        return f"ERROR listing files: {e}"
