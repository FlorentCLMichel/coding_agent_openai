from datetime import datetime
import json
import logging

from functions.get_files_info import *
from functions.get_file_content import *
from functions.create_dir import *
from functions.write_file import *
from functions.move_file import *
from functions.run_sh_command import *
from functions.run_python_file import *
from functions.compile_c import *
from functions.rust import *

safer_functions = {
    "get_files_info": get_files_info,
    "get_file_content": get_file_content,
    "create_dir": create_dir,
    "write_file": write_file,
    "move_file": move_file,
    "compile_cc": compile_cc,
    "compile_cxx": compile_cxx,
    "new_rust_project": new_rust_project,
    "build_rust_project": build_rust_project,
    "run_clippy": run_clippy,
}

unsafe_functions = {
    "run_sh_command": run_sh_command,
    "run_python_file": run_python_file,
    "run_rust_project": run_rust_project,
}

logging.basicConfig(
    filename='.function_calls.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

def call_function(function_name, function_args, verbose=False, working_directory='.', 
                  allow_unsafe_fun=False):
    
    # Log the function call
    logging.info(
        f"Function called: {function_name} | "
        f"Arguments: {function_args} | "
        f"Working Directory: {working_directory} | "
        f"Allow Unsafe Functions: {allow_unsafe_fun}"
    )

    function_args = json.loads(function_args)
    if verbose:
        print(f"→ Calling function: {function_name}({function_args})")
    if function_name in safer_functions.keys():
        function_args["working_directory"] = working_directory
        try: 
            return safer_functions[function_name](**function_args)
        except Exception as e:
            return f"ERROR calling the function {function_name}: {e}"
    elif (function_name in unsafe_functions.keys()) and allow_unsafe_fun:
        function_args["working_directory"] = working_directory
        try: 
            return unsafe_functions[function_name](**function_args)
        except Exception as e:
            return f"ERROR calling the function {function_name}: {e}"
    else:
        return f"ERROR: Unknown function: {function_name}",
