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
from functions.tools import tools

PROMPT_PREFIX = "\u276f "

HELP_MESSAGE = '''Available commands:
  /exit : leave the chat
  /file : load prompt from a file
  /help : print this help message
  /use_functions [0,1] : turn the ability to use functions on (1) or off (0)
  /verbose [0,1] : turn verbose mode on (1) or off (0)
  /wd <directory> : change the working directory
'''

commands = [
    '/exit', '/file', '/help', '/use_functions', '/verbose', '/wd',
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
    with open(file_name, "r") as file:
        return file.read()

def load_env_var(var: str, store: dict):
    var_up = var.upper()
    store[var] = environ.get(var_up)
    if not store[var]:
        print(f"\u2192 ERROR: Environment variable " + var_up + " not set")
        exit(1)

def initialize_client(variables: dict):
    try:
        client = OpenAI(
            base_url=variables["base_url"],
            api_key=variables["api_key"],
        )
        client.models.list()  # Example call to test the connection
        return client
    except Exception as e:
        print(f"\u2192 ERROR: Could not set-up the client: {e}")
        exit(1)

def handle_exit():
    exit(0)

def handle_help():
    print(HELP_MESSAGE)

def handle_file_command(user_query_split: list):
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
    try:
        if len(user_query_split) < 2:
            raise ValueError("Missing argument for /use_functions")
        use_functions = bool(int(user_query_split[1]))
        print(f"\u279c Ability to use functions {use_functions}")
        return use_functions
    except ValueError as e:
        raise Exception(f"\u279c ERROR: Invalid input for /use_functions: {e}")

def handle_verbose_command(user_query_split: list):
    try:
        if len(user_query_split) < 2:
            raise ValueError("Missing argument for /verbose")
        verbose = bool(int(user_query_split[1]))
        print(f"\u2192 Verbose mode {verbose}")
        return verbose
    except ValueError as e:
        raise ValueError(f"Invalid input for /verbose: {e}")

def handle_wd_command(user_query_split: list):
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

def process_user_query(user_query: str, use_functions: bool, verbose: bool, working_directory: str, client, variables: dict, input_list: list):
    reasoning = True
    while reasoning:
        reasoning = False
        try:
            response = client.responses.create(
                model=variables["model"],
                tools=tools if use_functions else [],
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
                output = call_function(item.name, item.arguments, verbose=verbose, working_directory=working_directory)
                input_list.append({
                    "type": "function_call_output",
                    "call_id": item.call_id,
                    "output": json.dumps({
                        "output": output
                    })
                })

    return response.output_text

def main():
    working_directory = "test"
    verbose = False
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

            response_text = process_user_query(user_query, use_functions, verbose, working_directory, client, variables, input_list)

            history_file.write('\n' + response_text + '\n\n')
            print('\n' + response_text + '\n')


if __name__ == "__main__":
    main()
