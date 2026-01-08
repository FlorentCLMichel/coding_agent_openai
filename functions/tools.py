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
]
