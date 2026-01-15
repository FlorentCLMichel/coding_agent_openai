# Simple OpenAI Coding Agent

This project implements a simple coding agent using the OpenAI Python API. The agent can interact with users, execute commands, and perform tasks based on the provided system prompt.

## Warning

This is an experimental implementation of a coding agent. It may Python code locally, compile C or C++ code, and has access to the file system within the working directory. Use with caution, as executing untrusted code can lead to unintended consequences, including data loss or security vulnerabilities. Always review the code and ensure it is safe before execution.

For security, you may disable function use by running `/use_functions 0`. 

The model can be given access to a shell by running `/allow_shell 1`. This obviously increases the risks. We recommend only using this in a sandboxed environment. 

**Risks:**
- Unintended file deletion or modification.
- Exposure of sensitive data.
- Execution of malicious code.

**Best Practices:**
- Run the agent in a sandboxed environment.
- Review all code before execution.
- Avoid using the agent with sensitive or production data.

## Features

- Interactive chat interface with the OpenAI model
- Support for custom commands to control the agent's behavior
- Integration with OpenAI's function calling API
- Working directory management for file operations

## Setup

### Prerequisites

- Python 3.x
- OpenAI Python library
- An API key from OpenAI or OpenRouter
- For compiling C/C++ code, a C/C++ compiler

### Environment Variables

The code requires three environment variables:

* `API_KEY`: Your OpenAI or OpenRouter API key
* `BASE_URL`: The URL where the model can be found
* `CC`: Command to use for compiling C code (default: `gcc`)
* `CXX`: Command to use for compiling C code (default: `g++`)
* `MODEL`: Name of the model to use

You can either set these explicitly or store them in a `.env` file. Here's an example `.env` file (replace `<your-API-key>` with your actual key):

```bash
API_KEY=<your-API-key>
BASE_URL=https://openrouter.ai/api/v1
CC="gcc"
CXX="g++"
MODEL=mistralai/devstral-2512:free
```

### Installation

1. Clone this repository:
   ```bash
   git clone <repository-url>
   cd <repository-directory>
   ```

2. Create and activate a virtual environment (optional but recommended):
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
   ```

3. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

Run the agent using:
```bash
python3 ./main.py
```

### Commands

The agent supports the following commands (all starting with `/`):

* `/help`: Print a help message
* `/exit`: Exit the program
* `/file <filename>`: Read the content of `<filename>` and treat it as a user query
* `/allow_shell [0,1]` : turn the ability to use a shell on (1) or off (0) (default: off)
* `/use_functions [0,1]` : turn the ability to use functions on (1) or off (0) (default: on)
* `/verbose [0,1]`: Set verbose mode on (1) or off (0) (default: off)
* `/wd <directory>`: Change the working directory

### System Prompt

The agent uses a system prompt defined in `system_prompt.md`. You can modify this file to change the agent's behavior.

### Chat History

The user queries and repplies for the model are logged in `.chat.history` for reference. The history of user inputs is logged in `.prompt_history`.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
