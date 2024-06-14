import os
from fuzzywuzzy import fuzz
import json
from collections import defaultdict

# --- Load Connection Map ---
script_path = os.path.abspath(os.path.dirname(__file__))
connection_map_path = os.path.join(script_path, "memories", "Memory_connecions_map.txt")

with open(connection_map_path, 'r', encoding='utf-8') as f:
    connection_map_data = f.read()

# --- Process Connection Map Data ---
connection_map = defaultdict(list)
for line in connection_map_data.splitlines():
    if "****" in line:
        current_folder_name = line.strip("****").strip()
    elif "  Path:" in line:
        path = line.strip("  Path:").strip()
        connection_map[current_folder_name].append(path)

# --- Functions for Memory Retrieval ---
def find_matching_folders(query, threshold=80):
    """Finds similar folders based on the query."""
    similar_folders = []
    for folder_name in connection_map:
        similarity_score = fuzz.ratio(query.lower(), folder_name.lower())
        if similarity_score >= threshold:
            similar_folders.append((folder_name, similarity_score, connection_map[folder_name]))  # Include paths
    return similar_folders

def retrieve_memory_frames(folder_paths, query, num_frames_before=1, num_frames_after=1):
    """Retrieves and orders memory frames from specified folders."""
    all_frames = []

    for folder_path in folder_paths:
        for root, _, files in os.walk(folder_path):
            for file in files:
                if file.endswith(".json"):
                    filepath = os.path.join(root, file)
                    with open(filepath, 'r') as f:
                        try:
                            frame_data = json.load(f)
                            # Basic keyword matching for now, can be enhanced
                            if query.lower() in frame_data.get("concise_summary", "").lower():
                                frame_data["filepath"] = filepath
                                all_frames.append(frame_data)
                        except json.JSONDecodeError:
                            print(f"Error: Invalid JSON in file: {filepath}")

    # Sort frames by timestamp
    sorted_frames = sorted(all_frames, key=lambda x: x.get("metadata", {}).get("creation_date", ""), reverse=True)

    # --- Frame Flow Reconstruction ---
    selected_frames = []
    for i, frame in enumerate(sorted_frames):
        if query.lower() in frame.get("concise_summary", "").lower():
            # Add the matching frame
            selected_frames.append(frame)

            # Add frames before
            for j in range(max(0, i - num_frames_before), i):
                selected_frames.append(sorted_frames[j])

            # Add frames after
            for j in range(i + 1, min(len(sorted_frames), i + num_frames_after + 1)):
                selected_frames.append(sorted_frames[j])

    return selected_frames

# --- Main Retrieval Loop ---
while True:
    user_query = input("Enter your memory query: ")

    # 1. Find Matching Folders
    matching_folders = find_matching_folders(user_query, threshold=70)  # Adjust threshold as needed

    if matching_folders:
        for folder_name, score, paths in matching_folders:
            print(f"Found matching folder '{folder_name}' with score {score}.")
            print(f"   Paths: {paths}")

        # 2. Retrieve and Display Memory Frames
        retrieved_frames = retrieve_memory_frames(
            [path for _, _, paths in matching_folders for path in paths],
            user_query,
            num_frames_before=1,  # Adjust these values as needed
            num_frames_after=1
        )

        if retrieved_frames:
            print(f"\nRetrieved {len(retrieved_frames)} memory frames:")
            for frame in retrieved_frames:
                print("-----------------------------------------")
                print(f"Filepath: {frame.get('filepath', 'N/A')}")
                print(f"Creation Date: {frame.get('metadata', {}).get('creation_date', 'N/A')}")
                print(f"Summary: {frame.get('summary', {}).get('concise_summary', 'N/A')}")
                print("-----------------------------------------")
        else:
            print("No memory frames found matching the query in the selected folders.")

    else:
        print("No matching folders found for the query.")

    # Add options to continue or exit the loop
    continue_search = input("Continue searching? (y/n): ").lower()
    if continue_search != 'y':
        break