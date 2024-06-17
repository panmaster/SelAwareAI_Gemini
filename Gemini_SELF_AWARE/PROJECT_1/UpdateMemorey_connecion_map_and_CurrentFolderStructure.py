import os
from collections import defaultdict
from fuzzywuzzy import fuzz
from datetime import datetime
import sys
import json

# --- Terminal Colors ---
class TerminalColors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    COLOR_CODES = {
        "red": FAIL,
        "green": OKGREEN,
        "yellow": WARNING,
        "blue": OKBLUE,
        "magenta": HEADER,
        "reset": ENDC
    }


def print_colored(text, color="white"):
    print(f"{TerminalColors.COLOR_CODES.get(color, '')}{text}{TerminalColors.COLOR_CODES['reset']}")


# --- Folder Management Functions ---
def find_similar_folders(folder_list):
    """Finds and returns a dictionary of similar folders."""
    print_colored("Finding similar folders...", "blue")
    similar_folders = defaultdict(list)
    total_combinations = len(folder_list) * (len(folder_list) - 1) // 2  # Total unique combinations
    completed_comparisons = 0  # Track comparisons made

    print_colored(f"  - Total folder combinations: {total_combinations}", "blue")

    # Stage 1: Partial Token Sort Ratio
    print_colored("    - Stage 1: Partial Token Sort Ratio", "blue")
    for i in range(len(folder_list)):
        for j in range(i + 1, len(folder_list)):
            folder_name_1, path_1 = folder_list[i]
            folder_name_2, path_2 = folder_list[j]

            completed_comparisons += 1

            progress_percent = int(completed_comparisons / total_combinations * 100)
            progress_bar = "[" + "#" * progress_percent + "-" * (100 - progress_percent) + "]"
            sys.stdout.write(f"\r      - {progress_bar} {progress_percent}% ")
            sys.stdout.flush()

            similarity_score = fuzz.partial_token_sort_ratio(folder_name_1, folder_name_2)
            similarity_threshold = 80

            if similarity_score >= similarity_threshold:
                similar_folders[folder_name_1].append(path_2)
                similar_folders[folder_name_2].append(path_1)

    # Stage 2: Partial Ratio
    print_colored("    - Stage 2: Partial Ratio", "blue")
    completed_comparisons = 0  # Reset for the second stage
    for i in range(len(folder_list)):
        for j in range(i + 1, len(folder_list)):
            folder_name_1, path_1 = folder_list[i]
            folder_name_2, path_2 = folder_list[j]

            completed_comparisons += 1

            progress_percent = int(completed_comparisons / total_combinations * 100)
            progress_bar = "[" + "#" * progress_percent + "-" * (100 - progress_percent) + "]"
            sys.stdout.write(f"\r      - {progress_bar} {progress_percent}% ")
            sys.stdout.flush()

            similarity_score = fuzz.partial_ratio(folder_name_1, folder_name_2)
            similarity_threshold = 70

            if similarity_score >= similarity_threshold:
                similar_folders[folder_name_1].append(path_2)
                similar_folders[folder_name_2].append(path_1)

    print("")  # Print a newline after the progress bar
    return similar_folders


def create_memory_connections_map(similar_folders, file_path):
    """Creates the Memory_connections_map.txt file."""
    with open(file_path, "w") as f:
        for folder_name, paths in similar_folders.items():
            f.write(f"**** {folder_name} ****\n")
            for path in paths:
                f.write(f"  Path: {path}\n")
            f.write("\n")


# --- Memory Synchronization Function ---
def synchronize_memories():
    """Checks folder structure and updates the memory connection map."""
    memories_path = os.path.join(os.getcwd(), "memories")  # Assuming script is in the same directory
    memory_connections_file = os.path.join(memories_path, "Memory_connections_map.txt")

    # 1. Check if memories folder exists:
    if not os.path.exists(memories_path):
        print_colored("Memories folder does not exist.", "red")
        return

    # 2. Get the folder list
    folder_list = []
    for root, dirs, _ in os.walk(memories_path):
        for dir_name in dirs:
            folder_list.append((dir_name, os.path.join(root, dir_name)))

    # 3. Find similar folders and update the connection map
    similar_folders = find_similar_folders(folder_list)
    create_memory_connections_map(similar_folders, memory_connections_file)

    print_colored("Memory connection map updated.", "green")


# --- Main Execution ---
if __name__ == "__main__":
    synchronize_memories()