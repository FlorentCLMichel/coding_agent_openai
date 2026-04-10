from dotenv import load_dotenv
from openai import OpenAI
from os import environ, path
from time import sleep

import openai
import json
import readline
import tiktoken

from prompt_toolkit import prompt
from prompt_toolkit.completion import WordCompleter, Completer, Completion
from prompt_toolkit.history import FileHistory
from prompt_toolkit.auto_suggest import AutoSuggestFromHistory
from prompt_toolkit.styles import Style

from shutil import copy2, copytree

from functions.interface import call_function
from functions.tools import safer_tools, unsafe_tools
from functions.utils import HISTORY_FILE, reprint

PROMPT_PREFIX = "\u276f "

HELP_MESSAGE = '''Available commands:
  /allow_unsafe_fun [0,1] : turn the ability to run unsafe functions on (1) or off (0) (default: OFF)
  /analyze : analyze the current conversation and report some metrics
  /exit : leave the chat
  /file <filename> : load prompt from a file
  /help : print this help message
  /load <filename> : load a conversation from a file
  /multiline [0,1] : turn multiline prompts on (1) off (0) (default: OFF)
  /reset_context : reset the context
  /save <filename> : save the current conversation in a file
  /skills : copy skill files to the working directory
  /system_prompt <filename> : load the system prompt from a file and reset the context
  /temperature <value> : change the temperature of the model
  /use_functions [0,1] : turn the ability to use functions on (1) or off (0) (default: ON)
  /verbose [0,1] : turn verbose mode on (1) or off (0) (default: OFF)
  /wd <directory> : change the working directory
'''

commands = [
    '/allow_unsafe_fun', '/analyze', '/exit', '/file', '/help', '/load', '/multiline', '/reset_context', 
    '/save', '/skills', '/system_prompt', '/temperature', '/use_functions', '/verbose', '/wd',
]

command_completer = WordCompleter(commands, sentence=True)

class CustomCompleter(Completer):
    def __init__(self, word_completer):
        self.word_completer = word_completer

    def get_completions(self, document, complete_event):
        if document.text.startswith('/') and not (' ' in document.text):
            all_completions = list(self.word_completer.get_completions(document, complete_event))
            for completion in all_completions:
                yield completion

custom_style = Style.from_dict({
    'prompt': '#ffffff',
    'input': '#ffffff',
})

def read_file(file_name: str) -> str:
    """
    Read the content of a file and return it as a string.
    
    Args:
        file_name (str): The name of the file to read.
    
    Returns:
        str: The content of the file.
    """
    with open(file_name, "r") as file:
        return file.read()

def load_env_var(var: str, store: dict, fun = lambda x: x):
    """
    Load an environment variable into a dictionary and check if it is set.
    
    Args:
        var (str): The name of the environment variable to load.
        store (dict): The dictionary to store the environment variable in.
    
    Raises:
        SystemExit: If the environment variable is not set.
    """
    var_up = var.upper()
    store[var] = fun(environ.get(var_up))
    if not store[var]:
        reprint(f"→ ERROR: Environment variable " + var_up + " not set")
        exit(1)

def initialize_client(variables: dict):
    """
    Initialize and return an OpenAI client using the provided configuration.
    
    Args:
        variables (dict): A dictionary containing the configuration variables for the client.
    
    Returns:
        OpenAI: An initialized OpenAI client.
    
    Raises:
        SystemExit: If the client cannot be initialized or the connection fails.
    """
    try:
        client = OpenAI(
            base_url=variables["base_url"],
            api_key=variables["api_key"],
        )
        client.models.list()  # Example call to test the connection
        return client
    except Exception as e:
        reprint(f"→ ERROR: Could not set-up the client: {e}")
        exit(1)

def handle_analyze(conversation: list):
    enc = tiktoken.get_encoding("o200k_base")
    num_tokens = {'system': 0, 'user': 0}
    for item in conversation:
        # Items may be dictionaries or Response objects depending on whether they come from a saved
        # conversation or directly from a model output. 
        if not isinstance(item, dict): 
            item = item.model_dump()
        role = item.get('role', 'unknown')
        content = item['content']
        if isinstance(content, list):
            for line in content:
                num_tokens[role] = num_tokens.get('role', 0) + len(enc.encode(line['text']))
        else: 
            num_tokens[role] = num_tokens.get('role', 0) + len(enc.encode(content))
    reprint("Estimated current token use:")
    for role in num_tokens:
        reprint(f"  {role}: {num_tokens[role]}")

def handle_multiline(user_query_split: list):
    """
    Handle the /multiline command to toggle multiline prompts.
    
    Args:
        user_query_split (list): A list of strings representing the user's query split by spaces.
    
    Returns:
        bool: The new state of the multiline flag.
    
    Raises:
        ValueError: If the argument is missing or invalid.
    """
    try:
        if len(user_query_split) < 2:
            raise ValueError("Missing argument for /multiline")
        multiline = bool(int(user_query_split[1]))
        reprint(f"→ Multiline prompts: {multiline}")
        return multiline
    except ValueError as e:
        raise ValueError(f"Invalid input for /multiline: {e}")

def handle_allow_unsafe_fun(user_query_split: list):
    """
    Handle the /allow_unsafe_fun command to toggle unsafe functions.
    
    Args:
        user_query_split (list): A list of strings representing the user's query split by spaces.
    
    Returns:
        bool: The new state of the allow_unsafe_fun flag.
    
    Raises:
        ValueError: If the argument is missing or invalid.
    """
    try:
        if len(user_query_split) < 2:
            raise ValueError("Missing argument for /allow_unsafe_fun")
        allow_unsafe_fun = bool(int(user_query_split[1]))
        reprint(f"→ Use of unsafe functions allowed: {allow_unsafe_fun}")
        return allow_unsafe_fun
    except ValueError as e:
        raise ValueError(f"Invalid input for /allow_unsafe_fun: {e}")

def handle_exit():
    """
    Exit the application.
    """
    exit(0)

def handle_help():
    """
    Display the help message to the user.
    """
    reprint(HELP_MESSAGE)

def handle_file_command(user_query_split: list) -> str:
    """
    Handle the /file command to read a file and return its content.
    
    Args:
        user_query_split (list): A list of strings representing the user's query split by spaces.
    
    Returns:
        str: The content of the file.
    
    Raises:
        Exception: If the file is not found, permission is denied, or an unexpected error occurs.
    """
    try:
        if len(user_query_split) < 2:
            raise ValueError("Missing argument for (file name)")
        fname = user_query_split[1]
        return read_file(fname)
    except FileNotFoundError:
        raise Exception(f"File not found: {fname}")
    except PermissionError:
        raise Exception(f"Permission denied for file: {fname}")
    except Exception as e:
        raise Exception(f"Unexpected error while reading file: {e}")

def handle_load_command(user_query_split: list):
    """
    Handle the /load command to load a conversation from a file.
    
    Args:
        user_query_split (list): A list of strings representing the user's query split by spaces.
    
    Returns:
        List: The loaded conversation.
    
    Raises:
        Exception: If the file is not found, permission is denied, or an unexpected error occurs.
    """
    try:
        if len(user_query_split) < 2:
            raise ValueError("Missing argument for (file name)")
        fname = user_query_split[1]
        with open(fname, "r", encoding="utf-8") as f:
            conversation = json.load(f)
            reprint(f"SYSTEM: File {fname} loaded successfully.")
            return conversation
    except FileNotFoundError:
        raise Exception(f"File not found: {fname}")
    except PermissionError:
        raise Exception(f"Permission denied for file: {fname}")
    except Exception as e:
        raise Exception(f"Unexpected error while reading file: {e}")

def json_serializable(obj):
    """Fallback to convert Pydantic/OpenAI objects to dicts."""
    if hasattr(obj, 'model_dump'):
        return obj.model_dump(exclude_none=True)
    if hasattr(obj, '__dict__'):
        return obj.__dict__
    return str(obj)

def handle_save_command(user_query_split: list, conversation: list):
    """
    Handle the /save command to save the conversation into a file.
    
    Args:
        user_query_split (list): A list of strings representing the user's query split by spaces.
    
    Raises:
        Exception: If the file is not found, permission is denied, or an unexpected error occurs.
    """
    try:
        if len(user_query_split) < 2:
            raise ValueError("Missing argument for (file name)")
        fname = user_query_split[1]
        with open(fname, "w", encoding="utf-8") as file:
            json.dump(conversation, file, indent=4, default=json_serializable)
            reprint(f"SYSTEM: Conversation saved to {fname}")
    except FileNotFoundError:
        raise Exception(f"File not found: {fname}")
    except PermissionError:
        raise Exception(f"Permission denied for file: {fname}")
    except Exception as e:
        raise Exception(f"Unexpected error while reading file: {e}")

def handle_skills_command(working_directory: str):
    """
    Handle the /use_functions command to allow the use of skills. 
    """
    # Copy skill files to the working directory
    copy2("SKILLS.md", working_directory + '/') 
    copytree("skills", working_directory + '/skills', dirs_exist_ok=True) 

    reprint("→ Skill use enabled (you will need to run this command again if changing the working directory)")
    
    # Add skills information to the system prompt
    with open("SKILLS.md") as file:
        return {"role": "system", "content": file.read()}

def handle_temperature_command(user_query_split: list, old_temperature: float):
    """
    Handle the /temperature command to change the model temperature.
    
    Args:
        user_query_split (list): A list of strings representing the user's query split by spaces.
    
    Returns:
        float: The new temperature.
    
    Raises:
        ValueError: If the argument is missing or invalid.
    """
    try:
        if len(user_query_split) < 2:
            raise ValueError("Missing argument for /temperature")
        temperature = float(user_query_split[1])
        if temperature < 0. or temperature > 2. :
            raise ValueError(f"The temperature must be between 0 and 2; got {temperature}. Reverting to {old_temperature}.")
        reprint(f"→ Model temperature {temperature}")
        return temperature
    except ValueError as e:
        raise ValueError(f"Invalid input for /temperature: {e}")

def handle_use_functions_command(user_query_split: list):
    """
    Handle the /use_functions command to toggle the ability to use functions.
    
    Args:
        user_query_split (list): A list of strings representing the user's query split by spaces.
    
    Returns:
        bool: The new state of the use_functions flag.
    
    Raises:
        Exception: If the argument is missing or invalid.
    """
    try:
        if len(user_query_split) < 2:
            raise ValueError("Missing argument for /use_functions")
        use_functions = bool(int(user_query_split[1]))
        reprint(f"→ Ability to use functions {use_functions}")
        return use_functions
    except ValueError as e:
        raise Exception(f"→ ERROR: Invalid input for /use_functions: {e}")

def handle_verbose_command(user_query_split: list):
    """
    Handle the /verbose command to toggle verbose mode.
    
    Args:
        user_query_split (list): A list of strings representing the user's query split by spaces.
    
    Returns:
        bool: The new state of the verbose flag.
    
    Raises:
        ValueError: If the argument is missing or invalid.
    """
    try:
        if len(user_query_split) < 2:
            raise ValueError("Missing argument for /verbose")
        verbose = bool(int(user_query_split[1]))
        reprint(f"→ Verbose mode {verbose}")
        return verbose
    except ValueError as e:
        raise ValueError(f"Invalid input for /verbose: {e}")

def handle_wd_command(user_query_split: list):
    """
    Handle the /wd command to change the working directory.
    
    Args:
        user_query_split (list): A list of strings representing the user's query split by spaces.
    
    Returns:
        str: The new working directory.
    
    Raises:
        Exception: If the argument is missing, the directory does not exist, or an error occurs.
    """
    try:
        if len(user_query_split) < 2:
            raise ValueError("Missing argument for /wd")
        new_directory = user_query_split[1]
        if not path.isdir(new_directory):
            raise FileNotFoundError(f"Directory does not exist: {new_directory}")
        reprint(f"→ New working directory: {new_directory}")
        return new_directory
    except Exception as e:
        raise Exception(f"→ ERROR: Could not change working directory: {e}")

def process_user_query(user_query: str, use_functions: bool, allow_unsafe_fun: bool,
                       verbose: bool, working_directory: str, client, variables: dict, 
                       conversation: list):
    """
    Process the user's query and generate a response using the OpenAI client.
    
    Args:
        user_query (str): The user's query.
        use_functions (bool): Whether to allow the use of functions in the response.
        allow_unsafe_fun (bool): Whether to allow the use of unsafe functions.
        verbose (bool): Whether to enable verbose mode.
        working_directory (str): The current working directory.
        client: The OpenAI client used to generate the response.
        variables (dict): A dictionary containing configuration variables.
        conversation (list): A list of input messages for the conversation.
    
    Returns:
        str: The generated response text.
    
    Raises:
        SystemExit: If an error occurs during the processing of the query.
    """
    wait_time_s = float(variables["time_between_queries_s"])
    if use_functions:
        tools = safer_tools
        if allow_unsafe_fun:
            tools += unsafe_tools
    else:
        tools = []
    finished = False
    while not finished:
        sleep(wait_time_s)
        try:
            response = client.responses.create(
                model=variables["model"],
                tools=tools,
                input=conversation,
                temperature=variables["temperature"],
            )

            if response.output_text:
                finished = True
            if not hasattr(response, "output"):
                raise ValueError("Invalid response structure: missing 'output' field")
        
        except openai.RateLimitError as e:
            reprint(f"→ ERROR: {e}")
            wait_time_s = 2*wait_time_s + float(variables["time_increment_s"])
            reprint(f"→ SYSTEM: Increasing wait time to {wait_time_s}s")
            continue

        except Exception as e:
            reprint(f"→ ERROR: {e}")
            return
        
        conversation += response.output

        for item in response.output:
            if not hasattr(item, "type"):
                continue
            if use_functions and item.type == "function_call":
                finished = False
                if not hasattr(item, "name") or not hasattr(item, "arguments"):
                    raise ValueError("Invalid function call structure")
                output = call_function(item.name, item.arguments, verbose=verbose, 
                                       working_directory=working_directory,
                                       allow_unsafe_fun=allow_unsafe_fun)
                if verbose:
                    reprint(f'→ Function output: {output}')
                conversation.append({
                    "type": "function_call_output",
                    "call_id": item.call_id,
                    "output": json.dumps({
                        "output": output
                    })
                })
                continue
            if item.type != 'message' and item.content:
                if verbose:
                    reprint(f'→ Response type `{item.type}`: {"\n".join(filter(None, map(lambda x: x.text.strip(), item.content)))}')
                continue
        
        final_response = response.output_text.strip()
        if final_response:
            reprint('\n💻 ' + final_response + '\n\n\a')

        wait_time_s = (wait_time_s + float(variables["time_between_queries_s"])) / 2.

def main():
    """
    Main function to run the prototype coding agent.
    
    This function initializes the environment, sets up the OpenAI client, and starts the interactive chat loop.
    """
    working_directory = "test"
    verbose = False
    allow_unsafe_fun = False
    use_functions = True
    multiline = False

    variables = {}
    load_dotenv()
    load_env_var("api_key", variables)
    load_env_var("model", variables)
    load_env_var("base_url", variables)
    load_env_var("temperature", variables, float)
    load_env_var("time_between_queries_s", variables)
    load_env_var("time_increment_s", variables)

    client = initialize_client(variables)

    system_prompt = read_file("system_prompt.md")
    conversation = [{"role": "system", "content": system_prompt}]

    # Initialize prompt_toolkit history
    history = FileHistory('.prompt_history')

    while True:
        try:
            # Use prompt_toolkit for user input
            user_query = prompt(
                PROMPT_PREFIX,
                completer=CustomCompleter(command_completer),
                history=history,
                auto_suggest=AutoSuggestFromHistory(),
                style=custom_style,
                complete_while_typing=True,
                multiline=multiline
            ).strip()
        except KeyboardInterrupt:
            continue  # Handle Ctrl+C gracefully
        except EOFError:
            break  # Handle Ctrl+D gracefully

        user_query_split = user_query.split()
        if not user_query_split:
            continue

        try:
            match user_query_split[0]:
                case '/allow_unsafe_fun':
                    allow_unsafe_fun = handle_allow_unsafe_fun(user_query_split)
                    continue
                case '/analyze':
                    handle_analyze(conversation)
                    continue
                case '/exit':
                    handle_exit()
                case '/help':
                    handle_help()
                    continue
                case '/file':
                    user_query = handle_file_command(user_query_split)
                case '/load':
                    conversation = handle_load_command(user_query_split)
                    continue
                case '/multiline':
                    multiline = handle_multiline(user_query_split)
                    continue
                case '/reset_context':
                    conversation = [{"role": "system", "content": system_prompt}]
                    reprint(f"→ SYSTEM: Context resetted")
                    continue
                case '/save':
                    handle_save_command(user_query_split, conversation)
                    continue
                case '/skills':
                    conversation.append(handle_skills_command(working_directory))
                    continue
                case '/system_prompt':
                    system_prompt = handle_file_command(user_query_split)
                    conversation = [{"role": "system", "content": system_prompt}]
                    reprint(f"→ SYSTEM: System prompt changed")
                    continue
                case '/temperature':
                    variables['temperature'] = handle_temperature_command(user_query_split, variables['temperature'])
                    continue
                case '/use_functions':
                    use_functions = handle_use_functions_command(user_query_split)
                    continue
                case '/verbose':
                    verbose = handle_verbose_command(user_query_split)
                    continue
                case '/wd':
                    working_directory = handle_wd_command(user_query_split)
                    continue
        except Exception as e:
            reprint(f"→ ERROR: {e}")
            continue

        with open(HISTORY_FILE, "a") as history_file:
            history_file.write(PROMPT_PREFIX + user_query + '\n\n')
        conversation.append({"role": "user", "content": user_query})

        process_user_query(user_query, use_functions, allow_unsafe_fun,
                           verbose, working_directory, client, variables, 
                           conversation)


if __name__ == "__main__":
    main()
