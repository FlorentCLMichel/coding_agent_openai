from dotenv import load_dotenv
from openai import OpenAI
from os import environ

import readline

PROMPT_PREFIX = "❯ "

HELP_MESSAGE = '''Available commands:
  /exit leave the chat
  /file load prompt from a file
  /help print this help message
'''

def read_file(fine_name):
    with open(fine_name, "r") as file:
        return file.read()

def main():

    load_dotenv()
    model = environ.get("MODEL")

    client = OpenAI(
      base_url=environ.get("BASE_URL"),
      api_key=environ.get("API_KEY"),
    )

    system_prompt = read_file("system_prompt.md")
    messages = [{"role": "system", "content": system_prompt}]

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
                    user_query = read_file(user_query_split[1])

            history_file.write(PROMPT_PREFIX + user_query + '\n')
            messages.append({"role": "user", "content": user_query})
            
            try:
                response = client.chat.completions.create(
                  model=model,
                  messages=messages,
                )
            except Exception as e: 
                print(f"ERROR: {e}")
                exit(1)
            
            reply = response.choices[0].message
            reply_content = '\n' + reply.content + '\n'
            history_file.write(reply_content + '\n')
            messages.append({"role": "assistant", "content": reply_content})
            print(reply_content)


if __name__ == "__main__":
    main()
