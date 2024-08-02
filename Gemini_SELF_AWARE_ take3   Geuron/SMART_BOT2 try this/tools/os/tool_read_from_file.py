tool_type_for_TOOL_MANAGER="all"


tool_read_from_file_short_description=""" Reads content from a file. 
        """

def tool_read_from_file(file_path: str, encoding: str = 'utf-8', mode: str = 'r') -> str:
    """
    Reads content from a file.

    Args:
        file_path (str): The path to the file to be read.
        encoding (str, optional): The encoding of the file. Defaults to 'utf-8'.
        mode (str, optional): The mode to open the file in. Defaults to 'r' (read).

    Returns:
        str: The content of the file, or an error message if the file cannot be read.
    """
    try:
        with open(file_path, mode, encoding=encoding) as f:
            content = f.read()
        return content
    except Exception as e:
        return f"Error reading file: {str(e)}"