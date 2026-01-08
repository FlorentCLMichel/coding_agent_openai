from functions.utils import *

import subprocess

CC = "gcc"
CXX = "g++"

def compile_cc(working_directory, args, dir_path='.') -> str :
    dir_path = os.path.join(working_directory, dir_path)
    if not(path_is_parent(working_directory, dir_path)):
        return f'ERROR: Cannot write "{dir_path}" as it is outside the permitted working directory {working_directory}'
    log_file_path = dir_path + "/log.txt"
    try:
        with open(log_file_path, 'w') as f:
            subprocess.call([CC, *args], cwd=dir_path, stderr=f, stdout=f)
            return f'Finished running the compiler; see log.txt for the log and potential errors'
    except Exception as e:
        return f"ERROR: writing to file: {e}"

def compile_cxx(working_directory, args, dir_path='.') -> str :
    dir_path = os.path.join(working_directory, dir_path)
    if not(path_is_parent(working_directory, dir_path)):
        return f'ERROR: Cannot write "{dir_path}" as it is outside the permitted working directory {working_directory}'
    log_file_path = dir_path + "/log.txt"
    try:
        with open(log_file_path, 'w') as f:
            subprocess.call([CXX, *args], cwd=dir_path, stderr=f, stdout=f)
            return f'Finished running the compiler; see log.txt for the log and potential errors'
    except Exception as e:
        return f"ERROR: writing to file: {e}"
