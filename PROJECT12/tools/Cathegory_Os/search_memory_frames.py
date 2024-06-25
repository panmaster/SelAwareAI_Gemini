tool_type_for_Tool_Manager = "reflection"
import os
import json
from termcolor import colored

def search_memory_frames(query: str, memories_folder_path: str = "../../memories/AiGenerated",
                        max_results: int = 10, importance_level: int = None,
                        timestamp_range: list = None, keyword_filter: list = None,
                        verbose: bool = False) -> list:
    """
    Searches memory frames within a specified folder based on criteria.

    Args:
        query: The search query string.
        memories_folder_path: The path to the folder containing memory frames. Defaults to "memories/AiGenerated".
        max_results: The maximum number of results to return. Defaults to 10.
        importance_level: Filter results by importance level (0-100). Defaults to None (no filtering).
        timestamp_range: Filter results by timestamp range (e.g., [start_timestamp, end_timestamp]). Defaults to None (no filtering).
        keyword_filter: Filter results by keywords (e.g., ["python", "machine learning"]). Defaults to None (no filtering).
        verbose:  Flag to enable verbose logging. Defaults to False.

    Returns:
        A list of memory frame paths matching the search criteria.
    """

    print(colored(f"Entering: search_memory_frames(...)", 'blue'))

    results = []

    for root, _, files in os.walk(memories_folder_path):
        for file in files:
            if not file.endswith(".json"):
                continue

            file_path = os.path.join(root, file)

            if verbose:
                print(colored(f"Checking file: {file_path}", 'yellow'))

            try:
                with open(file_path, "r", encoding="utf-8") as f:
                    memory_frame = json.load(f)

                # Importance Level Filter
                if importance_level is not None and \
                   int(memory_frame['memory_data']['importance']['importance_level']) != importance_level:
                    continue

                # Timestamp Range Filter
                if timestamp_range is not None:
                    timestamp = memory_frame['memory_data']['metadata']['creation_date'].split("_")[0]
                    if not (timestamp_range[0] <= timestamp <= timestamp_range[1]):
                        continue

                # Keyword Filter
                if keyword_filter is not None:
                    keywords = memory_frame['memory_data']['content']['keywords']
                    if not any(keyword in keywords for keyword in keyword_filter):
                        continue

                # Query Match
                if query.lower() in memory_frame['user_input'].lower() or \
                   query.lower() in memory_frame['introspection'].lower() or \
                   query.lower() in memory_frame['reflection'].lower() or \
                   query.lower() in memory_frame['action'].lower() or \
                   query.lower() in memory_frame['function_call_result'].lower() or \
                   query.lower() in memory_frame['emotions'].lower() or \
                   query.lower() in memory_frame['learning'].lower():
                    results.append(file_path)

                    if len(results) >= max_results:
                        print(colored(f"Maximum results reached: {max_results}", 'yellow'))
                        break

            except Exception as e:
                print(colored(f"Error processing file {file_path}: {e}", 'red'))

    print(colored(f"Exiting: search_memory_frames(...)", 'blue'))
    return results

search_memory_frames_description_json = {
    'function_declarations': [
        {
            'name': 'search_memory_frames',
            'description': 'Searches memory frames within a specified folder based on criteria.',
            'parameters': {
                'type_': 'OBJECT',
                'properties': {
                    'query': {'type_': 'STRING', 'description': 'The search query string.'},
                    'memories_folder_path': {'type_': 'STRING', 'description': 'The path to the folder containing memory frames. Defaults to "memories/AiGenerated".'},
                    'max_results': {'type_': 'INTEGER', 'description': 'The maximum number of results to return. Defaults to 10.'},
                    'importance_level': {'type_': 'INTEGER', 'description': 'Filter results by importance level (0-100). Defaults to None (no filtering).'},
                    'timestamp_range': {'type_': 'ARRAY', 'items': {'type_': 'STRING'}, 'description': 'Filter results by timestamp range (e.g., [start_timestamp, end_timestamp]). Defaults to None (no filtering).'},
                    'keyword_filter': {'type_': 'ARRAY', 'items': {'type_': 'STRING'}, 'description': 'Filter results by keywords (e.g., ["python", "machine learning"]). Defaults to None (no filtering).'},
                    'verbose': {'type_': 'BOOLEAN', 'description': 'Flag to enable verbose logging. Defaults to False.'}
                },
                'required': ['query']
            }
        }
    ]
}

search_memory_frames_description_short_str = "Searches memory frames within a specified folder based on criteria"