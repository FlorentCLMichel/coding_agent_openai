A simple agent using the OpenAI Python API.

## How to use

The code uses three environment variables: 

* `API_KEY`: your OpenAI or OpenRouter API key
* `BASE_URL`: where the model can be found
* `MODEL`: name of the model to use

They can either be set explicitly or stored in the file `.env`. An example of `.env` file is (replace <your-API-key> by the actual key):

```
API_KEY=<your-API-key>
BASE_URL=https://openrouter.ai/api/v1
MODEL=mistralai/devstral-2512:free
```

Once these are set, you can run

```
python3 ./main.py
```

User input will be sent to the model, except if the first word is one of the following commands (all starting with `/`): 

* `/exit`: exit the program
* `/file <filename>`: read the content of `<filename>` and treat is as user query
* `/help`: print a help message
* `/verbose [0,1]`: set verbose mode on (1) or off (0)
*  `/wd <directory>`: change the working directory
