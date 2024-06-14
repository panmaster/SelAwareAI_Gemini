
import  os
import  json

def get_directory_structure(directory):

    print("Entered get_directory_structure function with directory:", directory)
    directory_structure = {}

    for root, dirs, files in os.walk(directory):
        file_info = []
        for file in files:
            file_path = os.path.join(root, file)
            file_info.append({
                'filename': file,
                'size': os.path.getsize(file_path),
                'relative_path': os.path.relpath(file_path, directory),
                'full_path': file_path
            })
        directory_structure[os.path.relpath(root, directory)] = {
            'files': file_info,
            'folders': dirs
        }

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
                    'directory': {'type_': 'STRING', 'description': 'The path to the directory.'}
                },
                'required': ['directory']
            }
        }
    ]
}

get_directory_structure_description_short_str="Returns a dictionary representing the directory structure with file names, sizes, relative paths, and full paths."