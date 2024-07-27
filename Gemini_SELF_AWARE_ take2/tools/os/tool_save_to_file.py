tool_type_for_TOOL_MANAGER="os"
tool_save_to_file_short_description="Saves content to a file with the specified name and path."
import  os


def tool_save_to_file(content: str = None, file_name: str = 'NoName', file_path: str = None) -> dict:
    """
    Saves content to a file with the specified name and path.

    Args:
        content (str, optional): The content to be written to the file. Defaults to None, which will write an empty string.
        file_name (str, optional): The name of the file to be created. Defaults to 'NoName'.
        file_path (str, optional): The path to the directory where the file should be created. If None, the current working directory will be used. Defaults to None.

    Returns:
        dict: A dictionary containing the status of the operation, a message, and the full path to the file.
    """

    print(f"Entering: save_to_file(...)", 'blue')
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
        print(success_message, 'green')
        print(f"Exiting: save_to_file(...)", 'blue')
        return {"status": "success", "message": success_message, "file_path": full_path}

    except Exception as e:
        error_message = f"Failed to save file: {str(e)}"
        print(error_message, 'red')
        print(f"Exiting: save_to_file(...)", 'blue')
        return {"status": "failure", "message": error_message}