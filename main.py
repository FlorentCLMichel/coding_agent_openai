from dotenv import load_dotenv
from openai import OpenAI
from os import environ, path

import json
import readline

from prompt_toolkit import prompt
from prompt_toolkit.completion import WordCompleter, Completer, Completion
from prompt_toolkit.history import FileHistory
from prompt_toolkit.auto_suggest import AutoSuggestFromHistory
from prompt_toolkit.styles import Style

from functions.interface import call_function
from functions.tools import safer_tools, unsafe_tools

PROMPT_PREFIX = "\u276f "

HELP_MESSAGE = '''Available commands:
  /help : print this help message
  /exit : leave the chat
  /file : load prompt from a file
  /verbose [0,1] : turn verbose mode on (1) or off (0) (default: OFF)
  /wd <directory> : change the working directory
  /use_functions [0,1] : turn the ability to use functions on (1) or off (0) (default: ON)
  /allow_unsafe_fun [0,1] : turn the ability to run unsafe functions on (1) or off (0) (default: OFF)
'''

commands = [
    '/allow_unsafe_fun', '/exit', '/file', '/help', '/use_functions', '/verbose', '/wd',
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

def load_env_var(var: str, store: dict):
    """
    Load an environment variable into a dictionary and check if it is set.
    
    Args:
        var (str): The name of the environment variable to load.
        store (dict): The dictionary to store the environment variable in.
    
    Raises:
        SystemExit: If the environment variable is not set.
    """
    var_up = var.upper()
    store[var] = environ.get(var_up)
    if not store[var]:
        print(f"→ ERROR: Environment variable " + var_up + " not set")
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
        print(f"→ ERROR: Could not set-up the client: {e}")
        exit(1)

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
        print(f"\u2192 Use of unsafe functions allowed: {allow_unsafe_fun}")
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
    print(HELP_MESSAGE)

def handle_file_command(user_query_split: list):
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
            raise ValueError("Missing argument for /file")
        fname = user_query_split[1]
        return read_file(fname)
    except FileNotFoundError:
        raise Exception(f"File not found: {fname}")
    except PermissionError:
        raise Exception(f"Permission denied for file: {fname}")
    except Exception as e:
        raise Exception(f"Unexpected error while reading file: {e}")

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
        print(f"\u279c Ability to use functions {use_functions}")
        return use_functions
    except ValueError as e:
        raise Exception(f"\u279c ERROR: Invalid input for /use_functions: {e}")

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
        print(f"\u2192 Verbose mode {verbose}")
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
        print(f"\u279c New working directory: {new_directory}")
        return new_directory
    except Exception as e:
        raise Exception(f"ERROR: Could not change working directory: {e}")

def process_user_query(user_query: str, use_functions: bool, allow_unsafe_fun: bool,
                       verbose: bool, working_directory: str, client, variables: dict, 
                       input_list: list):
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
        input_list (list): A list of input messages for the conversation.
    
    Returns:
        str: The generated response text.
    
    Raises:
        SystemExit: If an error occurs during the processing of the query.
    """
    if use_functions:
        tools = safer_tools
        if allow_unsafe_fun:
            tools += unsafe_tools
    else:
        tools = []
    reasoning = True
    while reasoning:
        reasoning = False
        try:
            response = client.responses.create(
                model=variables["model"],
                tools=tools,
                input=input_list,
            )
            if not hasattr(response, "output"):
                raise ValueError("Invalid response structure: missing 'output' field")
        except Exception as e:
            print(f"\u2192 ERROR: {e}")
            exit(1)

        input_list += response.output

        if use_functions:
            for item in response.output:
                if not hasattr(item, "type") or item.type != "function_call":
                    continue
                if not hasattr(item, "name") or not hasattr(item, "arguments"):
                    raise ValueError("Invalid function call structure")
                reasoning = True
                output = call_function(item.name, item.arguments, verbose=verbose, 
                                       working_directory=working_directory,
                                       allow_unsafe_fun=allow_unsafe_fun)
                input_list.append({
                    "type": "function_call_output",
                    "call_id": item.call_id,
                    "output": json.dumps({
                        "output": output
                    })
                })

    return response.output_text

def main():
    """
    Main function to run the prototype coding agent.
    
    This function initializes the environment, sets up the OpenAI client, and starts the interactive chat loop.
    """
    working_directory = "test"
    verbose = False
    allow_unsafe_fun = False
    use_functions = True

    load_dotenv()
    variables = {}
    load_env_var("model", variables)
    load_env_var("base_url", variables)
    load_env_var("api_key", variables)

    client = initialize_client(variables)

    system_prompt = read_file("system_prompt.md")
    input_list = [{"role": "system", "content": system_prompt}]

    # Initialize prompt_toolkit history
    history = FileHistory('.prompt_history')

    with open(".chat.history", "a") as history_file:
        while True:
            try:
                # Use prompt_toolkit for user input
                user_query = prompt(
                    PROMPT_PREFIX,
                    completer=CustomCompleter(command_completer),
                    history=history,
                    auto_suggest=AutoSuggestFromHistory(),
                    style=custom_style,
                    complete_while_typing=True
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
                    case '/exit':
                        handle_exit()
                    case '/help':
                        handle_help()
                        continue
                    case '/file':
                        user_query = handle_file_command(user_query_split)
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
                print(f"→ ERROR: {e}")
                continue

            history_file.write(PROMPT_PREFIX + user_query + '\n')
            input_list.append({"role": "user", "content": user_query})

            response_text = process_user_query(user_query, use_functions, allow_unsafe_fun,
                                               verbose, working_directory, client, variables, 
                                               input_list)

            history_file.write('\n' + response_text + '\n\n')
            print('\n' + response_text + '\n')


if __name__ == "__main__":
    main()
