# TODO: add the other functions
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
]
