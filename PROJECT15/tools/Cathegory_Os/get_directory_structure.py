tool_type_for_Tool_Manager="all"


import os


def get_directory_structure(directory=None, include_files=True, include_dirs=True, file_extension=None,
                            include_contents=False, specific_file=None, levels_up=0, verbose=False):
    if verbose:
        print("Entered get_directory_structure function with directory:", directory)

    # Set default directory
    if directory is None or directory == '/':
        directory = os.getcwd()
        if verbose:
            print(f"Directory is set to current working directory: {directory}")

    # Traverse up the directory hierarchy if levels_up is specified
    for _ in range(levels_up):
        directory = os.path.dirname(directory)
        if verbose:
            print(f"Traversed up one level, new directory: {directory}")

    # Safety check for the directory path
    if not os.path.exists(directory) or not os.path.isdir(directory):
        raise ValueError(f"The directory '{directory}' is not valid or does not exist.")

    directory_structure = {}

    def get_file_info(file_path):
        file_info = {
            'filename': os.path.basename(file_path),
            'size': os.path.getsize(file_path),
            'relative_path': os.path.relpath(file_path, directory),
            'full_path': file_path
        }
        if include_contents:
            try:
                with open(file_path, 'r') as file:
                    file_info['contents'] = file.read()
            except Exception as e:
                file_info['contents'] = f"Error reading file: {e}"
        return file_info

    if specific_file:
        if os.path.isfile(specific_file):
            if verbose:
                print(f"Getting details for specific file: {specific_file}")
            return get_file_info(specific_file)
        else:
            raise ValueError(f"The specified file '{specific_file}' does not exist.")

    for root, dirs, files in os.walk(directory):
        file_info = []
        if include_files:
            for file in files:
                if file_extension and not file.endswith(file_extension):
                    continue
                file_path = os.path.join(root, file)
                file_info.append(get_file_info(file_path))

        if include_dirs:
            directory_structure[os.path.relpath(root, directory)] = {
                'files': file_info,
                'folders': dirs
            }
        else:
            if file_info:
                directory_structure[os.path.relpath(root, directory)] = {
                    'files': file_info
                }

    if verbose:
        print("About to return the directory structure with", len(directory_structure), "folders.")

    return directory_structure


get_directory_structure_description_json = {
    'function_declarations': [
        {
            'name': 'get_directory_structure',
            'description': 'Returns a dictionary representing the directory structure with file names, sizes, relative paths, and full paths.',
            'parameters': {
                'type_': 'OBJECT',
                'properties': {
                    'directory': {'type_': 'STRING',
                                  'description': 'The path to the directory. Defaults to the current working directory if None or / is provided.'},
                    'include_files': {'type_': 'BOOLEAN',
                                      'description': 'Flag to include files in the output. Default is True.'},
                    'include_dirs': {'type_': 'BOOLEAN',
                                     'description': 'Flag to include directories in the output. Default is True.'},
                    'file_extension': {'type_': 'STRING',
                                       'description': 'Specific file extension to include. Default is None.'},
                    'include_contents': {'type_': 'BOOLEAN',
                                         'description': 'Flag to include the contents of files in the output. Default is False.'},
                    'specific_file': {'type_': 'STRING',
                                      'description': 'Path to a specific file to get its details. Default is None.'},
                    'levels_up': {'type_': 'INTEGER',
                                  'description': 'Number of levels to traverse up from the specified or current directory. Default is 0.'},
                    'verbose': {'type_': 'BOOLEAN', 'description': 'Flag for verbose logging. Default is False.'}
                },
                'required': ['directory']
            }
        }
    ]
}



get_directory_structure_description_short_str = "Returns a dictionary representing the directory structure with file names, sizes, relative paths, and full paths. Includes options for filtering files, directories, file extensions, including file contents, and traversing up the directory hierarchy with a default to the current working directory."
