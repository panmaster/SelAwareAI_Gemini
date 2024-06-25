tool_type_for_Tool_Manager="action"

import os
import json
from termcolor import colored  # Import the termcolor library

def save_to_file(content: str = None, file_name: str = 'NoName', file_path: str = None) -> dict:

    print(colored(f"Entering: save_to_file(...)", 'blue'))
    if content is None:
        content = ""
    if file_path is None:
        full_path = os.path.join(os.getcwd(), file_name)
    else:
        full_path = os.path.join(file_path, file_name)

    try:
        with open(full_path, 'w', encoding='utf-8') as f:
            f.write(content)

        success_message = f"File saved successfully at: {full_path}"
        print(colored(success_message, 'green'))
        print(colored(f"Exiting: save_to_file(...)", 'blue'))
        return {"status": "success", "message": success_message, "file_path": full_path}

    except Exception as e:
        error_message = f"Failed to save file: {str(e)}"
        print(colored(error_message, 'red'))
        print(colored(f"Exiting: save_to_file(...)", 'blue'))
        return {"status": "failure", "message": error_message}


save_to_file_description_json = {
    'function_declarations': [
        {
            'name': 'save_to_file',
            'description': 'Saves content to a file.',
            'parameters': {
                'type_': 'OBJECT',
                'properties': {
                    'content': {'type_': 'STRING'},
                    'file_name': {'type_': 'STRING', 'description': 'The name of the file. Defaults to "NoName".'},
                    'file_path': {'type_': 'STRING', 'description': 'The path to save the file. Defaults to the current working directory if not provided.'}
                },
                'required': ['content', 'file_name']
            }
        }
    ]
}

save_to_file_description_short_str="Saves content to a file"