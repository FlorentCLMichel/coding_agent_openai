import json

from functions.get_files_info import *
from functions.get_file_content import *
from functions.create_dir import *
from functions.write_file import *
from functions.move_file import *
from functions.run_sh_command import *
from functions.run_python_file import *
from functions.compile_c import *

functions = {
    "get_files_info": get_files_info,
    "get_file_content": get_file_content,
    "create_dir": create_dir,
    "write_file": write_file,
    "move_file": move_file,
    "run_sh_command": run_sh_command,
    "run_python_file": run_python_file,
    "compile_cc": compile_cc,
    "compile_cxx": compile_cxx,
}

def call_function(function_name, function_args, verbose=False, working_directory='.', 
                  allow_python=False, allow_shell=False):
    function_args = json.loads(function_args)
    if verbose:
        print(f"Calling function: {function_name}({function_args})")
    if function_name == "run_sh_command" and not(allow_shell):
        return "ERROR: You do not have permission to run shell commands"
    if function_name == "run_python_file" and not(allow_python):
        return "ERROR: You do not have permission to run Python scripts"
    if function_name in functions.keys():
        function_args["working_directory"] = working_directory
        try: 
            return functions[function_name](**function_args)
        except e:
            return f"ERROR calling the function {function_name}: {e}"
    else:
        return f"ERROR: Unknown function: {function_name}",
