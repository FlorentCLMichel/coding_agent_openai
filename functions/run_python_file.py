from functions.config import TIMEOUT
from functions.utils import *
import subprocess

def run_python_file(working_directory, file_path, args="") -> str:
    rel_file_path = file_path
    file_path = os.path.join(working_directory, file_path)
    if not path_is_parent(working_directory, file_path):
        return f'ERROR: Cannot execute "{rel_file_path}" as it is outside the permitted working directory'
    if not os.path.exists(file_path):
        f'ERROR: File "{rel_file_path}" not found.'
    if not file_path.endswith('.py'):
        return f'ERROR: "{rel_file_path}" is not a Python file.'
    try:
        commands = ["python", file_path]
        if args:
            commands.extend(args.split())
        result = subprocess.run(
            commands,
            capture_output=True,
            text=True,
            timeout=TIMEOUT,
        )
        output = []
        if result.stdout:
            output.append(f"STDOUT:\n{result.stdout}")
        if result.stderr:
            output.append(f"STDERR:\n{result.stderr}")
        if result.returncode != 0:
            output.append(f"Process exited with code {result.returncode}")
        return "\n".join(output) if output else "No output produced."
    except Exception as e:
        return f"ERROR: executing Python file: {e}"
