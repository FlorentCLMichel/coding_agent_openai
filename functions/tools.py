tools = [
    {
        "type": "function",
        "name": "get_files_info",
        "description": "Lists files in the specified directory along with their sizes, constrained to the working directory.",
        "parameters": {
            "type": "object",
            "properties": {
                "directory": {
                    "type": "string",
                    "description": "The directory to list files from, relative to the working directory. If not provided, lists files in the working directory itself.",
                },
            },
            "required": ["directory"],
        },
    },
    {
        "type": "function",
        "name": "get_file_content",
        "description": "Read the content of the specified file, constrained to the working directory.",
        "parameters": {
            "type": "object",
            "properties": {
                "file_path": {
                    "type": "string",
                    "description": "Path to the file whose content should be read, relative to the working directory.",
                },
            },
            "required": ["file_path"],
        },
    },
    {
        "type": "function",
        "name": "create_dir",
        "description": "Create a new directory within the working directory.",
        "parameters": {
            "type": "object",
            "properties": {
                "dir_path": {
                    "type": "string",
                    "description": "Path to the new directory, relative to the working directory.",
                },
            },
            "required": ["dir_path"],
        },
    },
    {
        "type": "function",
        "name": "write_file",
        "description": "Write the specified content to the specified file, constrained to the working directory. If the file already exists, it is overwritten.",
        "parameters": {
            "type": "object",
            "properties": {
                "file_path": {
                    "type": "string",
                    "description": "The file to write the content to, relative to the working directory.",
                },
                "content": {
                    "type": "string",
                    "description": "The content to write to the file.",
                },
            },
            "required": ["file_path", "content"],
        },
    },
    {
        "type": "function",
        "name": "move_file",
        "description": "Move a file to a different location, constrained to the working directory.",
        "parameters": {
            "type": "object",
            "properties": {
                "source_path": {
                    "type": "string",
                    "description": "The original location of the file, relative to the working directory.",
                },
                "dest_path": {
                    "type": "string",
                    "description": "Destination for the file, relative to the working directory.",
                },
            },
            "required": ["source_path", "dest_path"],
        },
    },
    {
        "type": "function",
        "name": "run_sh_command",
        "description": "Run a shell command from the working directory.",
        "parameters": {
            "type": "object",
            "properties": {
                "cmd": {
                    "type": "string",
                    "description": "Command to run, including arguments",
                },
            },
            "required": ["cmd"],
        },
    },
    {
        "type": "function",
        "name": "run_python_file",
        "description": "Run the Python script in the specified file, constrained to the working directory.",
        "parameters": {
            "type": "object",
            "properties": {
                "file_path": {
                    "type": "string",
                    "description": "The file to execute, relative to the working directory.",
                },
                "args": {
                    "type": "string",
                    "description": "Space-separated list of arguments passed to the script.",
                    "default": "",
                },
            },
            "required": ["file_path"],
        },
    },
    {
        "type": "function",
        "name": "compile_cc",
        "description": "Run the gcc C compiler from the specified directory. The log is saved to log.txt.",
        "parameters": {
            "type": "object",
            "properties": {
                "args": {
                    "type": "string",
                    "description": "List of arguments passed to the compiler.",
                },
                "dir_path": {
                    "type": "string",
                    "description": "Path to the directory to run the compiler from, relative to the working directory.",
                    "default": ".",
                },
            },
            "required": ["args"],
        },
    },
    {
        "type": "function",
        "name": "compile_cxx",
        "description": "Run the g++ C++ compiler from the specified directory. The log is saved to log.txt.",
        "parameters": {
            "type": "object",
            "properties": {
                "args": {
                    "type": "string",
                    "description": "List of arguments passed to the compiler.",
                },
                "dir_path": {
                    "type": "string",
                    "description": "Path to the directory to run the compiler from, relative to the working directory.",
                    "default": ".",
                },
            },
            "required": ["args"],
        },
    },
    {
        "type": "function",
        "name": "new_rust_project",
        "description": "Create a new Rust project using Cargo. The log is saved to log.txt.",
        "parameters": {
            "type": "object",
            "properties": {
                "name": {
                    "type": "string",
                    "description": "Name of the project.",
                },
                "dir_path": {
                    "type": "string",
                    "description": "Path to the directory where the project should be created, relative to the working directory.",
                    "default": ".",
                },
                "args": {
                    "type": "string",
                    "description": "List of additional arguments passed to Cargo.",
                    "default": "",
                },
            },
            "required": ["name"],
        },
    },
    {
        "type": "function",
        "name": "build_rust_project",
        "description": "Build an existing Rust project using Cargo. The log is saved to log.txt.",
        "parameters": {
            "type": "object",
            "properties": {
                "name": {
                    "type": "string",
                    "description": "Name of the project.",
                },
                "dir_path": {
                    "type": "string",
                    "description": "Path to the directory where the project is located, relative to the working directory.",
                    "default": ".",
                },
                "args": {
                    "type": "string",
                    "description": "List of additional arguments passed to Cargo.",
                    "default": "",
                },
            },
            "required": ["name"],
        },
    },
    {
        "type": "function",
        "name": "run_rust_project",
        "description": "Run an existing Rust project using Cargo. The log is saved to log.txt.",
        "parameters": {
            "type": "object",
            "properties": {
                "name": {
                    "type": "string",
                    "description": "Name of the project.",
                },
                "dir_path": {
                    "type": "string",
                    "description": "Path to the directory where the project is located, relative to the working directory.",
                    "default": ".",
                },
                "args": {
                    "type": "string",
                    "description": "List of additional arguments passed to Cargo.",
                    "default": "",
                },
            },
            "required": ["name"],
        },
    },
    {
        "type": "function",
        "name": "run_clippy",
        "description": "Run the Clippy linter for a Rust project. The log is saved to log.txt.",
        "parameters": {
            "type": "object",
            "properties": {
                "name": {
                    "type": "string",
                    "description": "Name of the project.",
                },
                "dir_path": {
                    "type": "string",
                    "description": "Path to the directory where the project is located, relative to the working directory.",
                    "default": ".",
                },
                "args": {
                    "type": "string",
                    "description": "List of additional arguments passed to Clippy.",
                    "default": "",
                },
            },
            "required": ["name"],
        },
    },
]
