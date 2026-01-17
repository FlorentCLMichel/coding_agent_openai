from functions.config import TIMEOUT
from functions.utils import *
import subprocess

def run_sh_command(working_directory, cmd) -> str:
    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            shell=True,
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
        return f"ERROR: executing shell command: {e}"
