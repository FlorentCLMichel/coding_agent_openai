# Simple OpenAI Coding Agent

This project implements a simple coding agent using the OpenAI Python API. The agent can interact with users, execute commands, and perform tasks based on the provided system prompt.

## Warning

This is an experimental implementation of a coding agent. It may compile C, C++, or Rust code and has access to the file system within the working directory. Use with caution, as executing untrusted code can lead to unintended consequences, including data loss or security vulnerabilities. Always review the code and ensure it is safe before execution. 

In principle, the agent only has access to the content of the working directory (by default, `test`; it can be changed with the `/wd` command). **Ensure the working directory is isolated and contains no sensitive data.** Please note that there is no guarantee that an error in the code may not allow access to files outside the working directory.

For additional security, you may disable function use by running `/use_functions 0`. 

The model can be given access to a shell and allowed to run Python or Rust code (by running `/allow_unsafe_fun 1`). **Letting an AI model run arbitrary code is fundamentally insecure.** We recommend not using these features unless running the agent in a sandboxed environment. 

**By default, shell access and code execution are disabled. Do not enable these features unless you fully understand the risks and are running in a sandboxed environment.**

### Risks

- **Unintended File Modification/Deletion**: The agent may overwrite or delete files in the working directory.
- **Data Exposure**: Sensitive data in the working directory could be read or leaked.
- **Malicious Code Execution**: Enabling shell or Python execution allows arbitrary code to run, which could compromise your system.

### Best Practices

1. **Sandboxing**: Run the agent in a sandboxed environment (e.g., Docker container or VM) with:
   - Restricted network access.
   - A read-only filesystem where possible.
   - Minimal permissions.
2. **Isolate the Working Directory**: Ensure the working directory contains no sensitive data and is isolated from the rest of your system.
3. **Review Logs**: Audit the agent’s actions by reviewing `.chat.history`, `.prompt_history`, and `.function_calls.log`.
4. **Disable High-Risk Features**: Do not use `/allow_unsafe_fun 1` to enable shell and code execution unless you are sure you know what you are doing.

To mitigate risks, we recommend at least [running the agent from a limited user](#Running-the-agent-from-a-temporary-user-in-Linux). For additional security, consider using a [Docker](https://www.docker.com/) or [Bubblewrap](https://github.com/containers/bubblewrap) container, or running the agent in a virtual machine with non sensitive information.

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
- For compiling C/C++ code, a C/C++ compiler such as [gcc/g++](https://gcc.gnu.org/)
- For creating and building Rust projects, the [Rust toolchain](https://rust-lang.org/tools/install/)

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
* `/verbose [0,1]`: Set verbose mode on (1) or off (0) (default: off)
* `/wd <directory>`: Change the working directory
* `/use_functions [0,1]` : turn the ability to use functions on (1) or off (0) (default: on)
* `/allow_unsafe_fun [0,1]` : turn the ability to run unsafe functions on (1) or off (0) (default: off)

### System Prompt

The agent uses a system prompt defined in `system_prompt.md`. You can modify this file to change the agent's behavior.

### Chat History

The user queries and repplies for the model are logged in `.chat.history` for reference. The history of user inputs is logged in `.prompt_history` and the log of function calls from the model in `.function_calls.log`.


## Running the agent from a temporary user in Linux

In this section we sketch how to run the agent from a temporary user account on Linux to reduce security risks. Steps 1 to 4 and 6 are only required the first time you use the agent from a new user account. Steps 5, 7, and 8 are required each time the agent is run (although step 7 may be skipped if saving a file `.env` with all the required [environment variables](#Environment-Variables)). Step 9 is optional. (For each command, `sudo` may be omitted if loged-in as root.)

1. Create a temporary user:
    ```
    sudo adduser <temp_user>
    ```

2. Copy the repository content to a new directory in the user `home` directory:
    ```
    sudo mkdir /home/<temp_user>/<agent_dir>
    sudo cp -r * /home/<temp_user>/<agent_dir>
    sudo chown <temp_user> -R /home/temp_user/<agent_dir>
    ```

3. Log-in as the temporary user:
    ```
    su - <temp_user>
    ```
4. Create a virtual environment:
    ```
    python3 -m venv <virtual_env>
    ```

5. Activate the virtual environment and move to the agent directory:
    ```
    source <virtual_env>/bin/activate
    cd <agent_dir>
    ```

6. Install the required dependencies:
    ```
    pip3 install -r requirements.txt
    ```

7. Set the required [environment variables](#Environment-Variables)

8. Run the agent:
    ```
    python3 ./main.py
    ```

9. To delete the user, run the following command from a (different) user with sudo priviledge:
    ```
    sudo deluser --remove-home <temp_user>
    ```

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
