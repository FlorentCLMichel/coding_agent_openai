import subprocess

from functions.utils import *

def new_rust_project(working_directory, name, dir_path='.', args='') -> str :
    project_path = dir_path + '/' + name
    project_path = os.path.join(working_directory, project_path)
    if not(path_is_parent(working_directory, project_path)):
        return f'ERROR: Cannot write "{project_path}" as it is outside the permitted working directory {working_directory}'
    try:
        log_file_path = dir_path + "/log.txt"
        with open(working_directory + '/' + log_file_path, 'w') as f:
            if subprocess.call(['cargo', 'new', name, *args.split()], cwd=working_directory+'/'+dir_path, stderr=f, stdout=f):
                return f'ERROR: See {log_file_path} for details'
            return f'Created Rust project {name} in directory {dir_path}; see {log_file_path} for the log and potential errors'
    except Exception as e:
        return f"ERROR: writing to file: {e}"

def build_rust_project(working_directory, name, dir_path='.', args='') -> str :
    project_path = dir_path + '/' + name
    project_path = os.path.join(working_directory, project_path)
    if not(path_is_parent(working_directory, project_path)):
        return f'ERROR: Cannot write "{project_path}" as it is outside the permitted working directory {working_directory}'
    if not(os.path.isdir(project_path)):
        return f'ERROR: "{project_path}" is not a directory'
    try:
        log_file_path = dir_path + "/log.txt"
        with open(working_directory + '/' + log_file_path, 'w') as f:
            if subprocess.call(['cargo', 'build', *args.split()], cwd=project_path, stderr=f, stdout=f):
                return f'ERROR: See {log_file_path} for details'
            return f'Built Rust project {name} in directory {dir_path}; see {log_file_path} for the log and potential errors'
    except Exception as e:
        return f"ERROR: writing to file: {e}"

def run_rust_project(working_directory, name, dir_path='.', args='') -> str :
    project_path = dir_path + '/' + name
    project_path = os.path.join(working_directory, project_path)
    if not(path_is_parent(working_directory, project_path)):
        return f'ERROR: Cannot write "{project_path}" as it is outside the permitted working directory {working_directory}'
    if not(os.path.isdir(project_path)):
        return f'ERROR: "{project_path}" is not a directory'
    try:
        log_file_path = dir_path + "/log.txt"
        with open(working_directory + '/' + log_file_path, 'w') as f:
            if subprocess.call(['cargo', 'run', *args.split()], cwd=project_path, stderr=f, stdout=f):
                return f'ERROR: See {log_file_path} for details'
            return f'Ran Rust project {name} in directory {dir_path}; see {log_file_path} for the log and potential errors'
    except Exception as e:
        return f"ERROR: writing to file: {e}"

def run_clippy(working_directory, name, dir_path='.', args='') -> str :
    project_path = dir_path + '/' + name
    project_path = os.path.join(working_directory, project_path)
    if not(path_is_parent(working_directory, project_path)):
        return f'ERROR: Cannot write "{project_path}" as it is outside the permitted working directory {working_directory}'
    if not(os.path.isdir(project_path)):
        return f'ERROR: "{project_path}" is not a directory'
    try:
        log_file_path = dir_path + "/log.txt"
        with open(working_directory + '/' + log_file_path, 'w') as f:
            if subprocess.call(['cargo', 'clippy', *args.split()], cwd=project_path, stderr=f, stdout=f):
                return f'ERROR: See {log_file_path} for details'
            return f'Ran Clippy for project {name} in directory {dir_path}; see {log_file_path} for the log and potential errors'
    except Exception as e:
        return f"ERROR: writing to file: {e}"
