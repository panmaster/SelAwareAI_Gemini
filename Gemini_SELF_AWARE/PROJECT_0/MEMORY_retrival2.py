import os
import json
import re
from whoosh import index
from whoosh.fields import Schema, TEXT, ID, NUMERIC
from whoosh.qparser import MultifieldParser
from fuzzywuzzy import fuzz
from collections import defaultdict
import tempfile


# Define schema for Whoosh index
def create_schema():
    return Schema(
        filepath=ID(stored=True),
        creation_date=TEXT(stored=True),
        concise_summary=TEXT(stored=True),
        description=TEXT,
        keywords=TEXT,
        entities=TEXT,
        main_topic=TEXT,
        input=TEXT,
        response1=TEXT,
        response2=TEXT,
        importance_level=NUMERIC(stored=True),
        strength_of_matching=NUMERIC(stored=True)
    )


# Load connection map from a file
def load_connection_map(connection_map_path):
    connection_map = defaultdict(list)
    if os.path.exists(connection_map_path):
        with open(connection_map_path, 'r', encoding='utf-8') as file:
            content = file.read()
            folder_matches = re.findall(r'\*\*\*\*(.*?)\*\*\*\*(.*?)Path:\s*(.*?)\n', content, re.DOTALL)
            for match in folder_matches:
                folder_name, _, folder_path = match
                connection_map[folder_name.strip()].append(folder_path.strip())
    return connection_map


# Index memory frames using Whoosh
def index_memory_frames(schema, index_dir):
    if not os.path.exists(index_dir):
        os.mkdir(index_dir)

    ix = index.create_in(index_dir, schema)
    writer = ix.writer()

    frames_indexed = 0
    for root, _, files in os.walk("memories"):
        for file in files:
            if file.endswith(".json"):
                file_path = os.path.join(root, file)

                try:
                    with open(file_path, 'r', encoding='utf-8') as json_file:
                        frame_data = json.load(json_file)

                        # Extract importance level and strength of matching for Whoosh indexing
                        importance_level = int(
                            frame_data.get('memory_data', {}).get('importance', {}).get('importance_level', '0'))
                        strength_of_matching = int(
                            frame_data.get('memory_data', {}).get('storage', {}).get('memory_folders_storage', [{}])[
                                0].get('probability', '0'))

                        writer.add_document(
                            filepath=file_path,
                            creation_date=frame_data.get('metadata', {}).get('creation_date', 'N/A'),
                            concise_summary=frame_data.get('summary', {}).get('concise_summary', 'N/A'),
                            description=frame_data.get('summary', {}).get('description', ''),
                            keywords=frame_data.get('content', {}).get('keywords', ''),
                            entities=frame_data.get('content', {}).get('entities', ''),
                            main_topic=frame_data.get('core', {}).get('main_topic', ''),
                            input=frame_data.get('input', ''),
                            response1=frame_data.get('response1', ''),
                            response2=frame_data.get('response2', ''),
                            importance_level=importance_level,
                            strength_of_matching=strength_of_matching
                        )
                        frames_indexed += 1
                except json.JSONDecodeError as e:
                    print(f"Error decoding JSON file {file_path}: {e}")

    writer.commit()
    print(f"Indexed {frames_indexed} memory frames.")


# Search memory frames using Whoosh
def search_memory_frames(ix, query):
    with ix.searcher() as searcher:
        parser = MultifieldParser(
            ["creation_date", "concise_summary", "description", "keywords", "entities", "main_topic", "input",
             "response1", "response2"],
            schema=ix.schema
        )
        myquery = parser.parse(query)
        results = searcher.search(myquery, limit=None)
        return [dict(hit) for hit in results]


# Retrieve contextual memory frames around a main frame
def retrieve_contextual_frames(memory_frames, main_frame_index, num_frames_before=1, num_frames_after=1):
    selected_frames = []
    start_index = max(0, main_frame_index - num_frames_before)
    end_index = min(len(memory_frames), main_frame_index + num_frames_after + 1)
    selected_frames.extend(memory_frames[start_index:end_index])
    return selected_frames


# Find similar folders based on a query using fuzzy matching
def find_similar_folders(connection_map, query, threshold=80):
    similar_folders = {}
    for folder_name, folder_paths in connection_map.items():
        similarity_score = fuzz.token_sort_ratio(folder_name, query)
        if similarity_score >= threshold:
            similar_folders[folder_name] = folder_paths
    return similar_folders


# Memory retrieval strategies
def retrieve_by_importance(memory_frames, threshold=50):
    return [frame for frame in memory_frames if frame.get('importance_level', 0) >= threshold]


def retrieve_by_strength(memory_frames, threshold=50):
    return [frame for frame in memory_frames if frame.get('strength_of_matching', 0) >= threshold]


def retrieve_by_folder_match(connection_map, query, threshold=80):
    return find_similar_folders(connection_map, query, threshold)


# Main retrieval process
def process_retrieval(connection_map, ix):
    while True:
        user_query = input("Enter your memory query: ")

        matching_folders = retrieve_by_folder_match(connection_map, user_query)

        if matching_folders:
            for folder_name, paths in matching_folders.items():
                print(f"Found matching folder '{folder_name}' with paths: {paths}")

            results = search_memory_frames(ix, user_query)
            important_frames = retrieve_by_importance(results)
            strong_frames = retrieve_by_strength(important_frames)

            if strong_frames:
                print(f"\nRetrieved {len(strong_frames)} strong and important memory frames:")
                main_frame_index = 0  # Assuming the first frame is the best match
                contextual_frames = retrieve_contextual_frames(strong_frames, main_frame_index)
                for frame in contextual_frames:
                    print("-----------------------------------------")
                    print(f"Filepath: {frame.get('filepath', 'N/A')}")
                    print(f"Creation Date: {frame.get('creation_date', 'N/A')}")
                    print(f"Summary: {frame.get('concise_summary', 'N/A')}")
                    print("-----------------------------------------")
            else:
                print("No strong and important memory frames found matching the query.")

        else:
            print("No matching folders found for the query.")

        if input("Continue searching? (y/n): ").lower() != 'y':
            break


# Main function
def main():
    script_path = os.path.abspath(os.path.dirname(__file__))
    connection_map_path = os.path.join(script_path, "memories", "Memory_connections_map.txt")
    connection_map = load_connection_map(connection_map_path)

    with tempfile.TemporaryDirectory() as index_dir:  # Using a temporary directory to store the index files
        schema = create_schema()
        index_memory_frames(schema, index_dir)
        ix = index.open_dir(index_dir)
        process_retrieval(connection_map, ix)


if __name__ == "__main__":
    main()