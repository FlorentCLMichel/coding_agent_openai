from dotenv import load_dotenv
from openai import OpenAI
from os import environ

import json
import readline

from functions.interface import call_function
from functions.tools import tools

PROMPT_PREFIX = "❯ "

HELP_MESSAGE = '''Available commands:
  /exit : leave the chat
  /file : load prompt from a file
  /help : print this help message
  /use_functions [0,1] : turn the ability to use functions on (1) or off (0)
  /verbose [0,1] : turn verbose mode on (1) or off (0)
  /wd <directory> : change the working directory
'''

def read_file(file_name):
    with open(file_name, "r") as file:
        return file.read()


def main():
    working_directory="test"
    verbose=False
    use_functions=True

    load_dotenv()
    model = environ.get("MODEL")

    client = OpenAI(
      base_url=environ.get("BASE_URL"),
      api_key=environ.get("API_KEY"),
    )

    system_prompt = read_file("system_prompt.md")
    input_list = [{"role": "system", "content": system_prompt}]
    
    with open(".chat.history", "a") as history_file:
        while True:
            user_query = input(PROMPT_PREFIX).strip()
            user_query_split = user_query.split()
            match user_query_split[0]: 
                case '/exit':
                    exit(0)
                case '/help':
                    print(HELP_MESSAGE)
                    continue
                case '/file':
                    try:
                        user_query = read_file(user_query_split[1])
                    except Exception as e: 
                        print(f"→ Could not parse the query: {e}")
                        continue
                case '/use_functions':
                    try:
                        use_functions = bool(int(user_query_split[1]))
                        print(f"→ Ability to use functions {use_functions}")
                    except Exception as e: 
                        print(f"→ Could not parse the input: {e}")
                        continue
                    continue
                case '/verbose':
                    try:
                        verbose = bool(int(user_query_split[1]))
                        print(f"→ Verbose mode {verbose}")
                    except Exception as e: 
                        print(f"→ Could not parse the input: {e}")
                        continue
                    continue
                case '/wd':
                    try:
                        working_directory = user_query_split[1]
                        print(f"→ New working directory: {working_directory}")
                    except Exception as e: 
                        print(f"→ Could not parse the input: {e}")
                        continue
                    continue
            
            history_file.write(PROMPT_PREFIX + user_query + '\n')
            input_list.append({"role": "user", "content": user_query})
    
            reasoning = True
            while reasoning:
                reasoning = False
                try:
                    response = client.responses.create(
                        model=model,
                        tools= tools if use_functions else [],
                        input=input_list,
                    )
                except Exception as e: 
                    print(f"ERROR: {e}")
                    exit(1)
    
                input_list += response.output
    
                if use_functions:
                    for item in response.output:
                        if item.type == "function_call":
                            reasoning = True
                            output = call_function(item.name, item.arguments, verbose=verbose, working_directory=working_directory)
                            input_list.append({
                                "type": "function_call_output",
                                "call_id": item.call_id,
                                "output": json.dumps({
                                  "output": output
                                })
                            })
             
            history_file.write('\n' + response.output_text + '\n\n')
            print('\n' + response.output_text + '\n')

if __name__ == "__main__":
    main()
