tool_type_for_Tool_Manager = "all"
import  os
import  json
def summarize_files_contents(file_paths):

    print("Entered summarize_files_contents function with", len(file_paths), "file paths.")
    summaries = []
    for file_path in file_paths:
        print("Processing file:", file_path)
        summary = {}
        try:
            with open(file_path, 'r') as file:
                content = file.read()
                summary['path'] = file_path
                summary['content'] = content
        except Exception as e:
            summary['path'] = file_path
            summary['error'] = str(e)
        summaries.append(summary)

    print("About to return the summaries for", len(summaries), "files.")
    return summaries

summarize_files_contents_description_json = {
    'function_declarations': [
        {
            'name': 'summarize_files_contents',
            'description': 'Opens and summarizes the content of multiple files.',
            'parameters': {
                'type_': 'OBJECT',
                'properties': {
                    'file_paths': {'type_': 'ARRAY', 'items': {'type_': 'STRING'}, 'description': 'A list of file paths.'}
                },
                'required': ['file_paths']
            }
        }
    ]
}

summarize_files_contents_description_short_str="Opens and summarizes the content of multiple files.'"