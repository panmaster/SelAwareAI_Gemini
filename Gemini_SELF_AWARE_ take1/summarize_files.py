import os
from rich import print
from rich.table import Table
from rich.panel import Panel

# Constants
SUMMARY_FILENAME = "OLDsummarisation.txt"
CONTENT_LIMIT = 500000
BASE_FILE_LIMIT = 100
CURRENT_FOLDER_LIMIT = 100
MEMORY_MAP_LIMIT = 10
FLAT_MODE = True
INCLUDE_MEMORY_FRAMES = False  # Set to True to include files with 'MemoryFrames' in their names

# Exclude files from the summary
EXCLUDED_FILES = [
    "OLDsummarisation.txt",
    os.path.basename(__file__)  # Exclude the current script file
]

def summarize_directory(directory, limit=100):
    """Summarizes a directory's files and subdirectories, applying limits."""

    summary_filepath = os.path.join(directory, SUMMARY_FILENAME)

    with open(summary_filepath, "w", encoding="utf-8") as summary_file:
        write_summary_to_file(summary_file, directory, limit)

    print(f"[bold green]Summary file created: '{summary_filepath}'[/]")
    print_summary_from_file(summary_filepath)

    # Count and print the number of lines in the summary file
    line_count = count_lines_in_file(summary_filepath)
    print(f"[bold blue]Total lines in summary file: {line_count}[/]")

def write_summary_to_file(summary_file, directory, limit=100):
    """Writes the summary to the specified file."""

    summary_file.write(f"## Summary of Files and Directories in '{directory}'\n\n")

    for item in os.listdir(directory):
        item_path = os.path.join(directory, item)

        if os.path.isfile(item_path) and item not in EXCLUDED_FILES:
            if not INCLUDE_MEMORY_FRAMES and 'MemoryFrames' in item:
                continue
            # Write file info to file
            summary_file.write(f"File: {item} ({item_path})\n")

            # Write file content snippet with appropriate limits
            if item == "MEMORY_initializer.py" or item == "Memory_connections_map.txt":
                # Apply MEMORY_MAP_LIMIT here
                write_limited_file_content(summary_file, item_path, MEMORY_MAP_LIMIT)
            elif item == "BaseFileStructure.txt":
                write_file_content(summary_file, item_path, BASE_FILE_LIMIT)
            elif item == "CurrentFolderStructure.txt":
                write_file_content(summary_file, item_path, CURRENT_FOLDER_LIMIT)
            else:
                write_file_content(summary_file, item_path, limit)

        elif os.path.isdir(item_path):
            # Recursively write subdirectories with appropriate limits
            summary_file.write(f"\nSubdirectory: {item}\n")
            if item == "BaseFileStructure":
                write_summary_to_file(summary_file, item_path, BASE_FILE_LIMIT)
            elif item == "CurrentFolderStructure":
                write_summary_to_file(summary_file, item_path, CURRENT_FOLDER_LIMIT)
            else:
                write_summary_to_file(summary_file, item_path, limit)

def write_file_content(summary_file, file_path, limit):
    """Writes a limited snippet of file content or full content if FLAT_MODE is True."""
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.readlines()
            if FLAT_MODE:
                limited_content = content
            else:
                limited_content = content[:limit]
            summary_file.write(
                f"Content (First {len(limited_content)} lines):\n{''.join(limited_content)}\n\n"
            )
    except UnicodeDecodeError as e:
        summary_file.write(f"Error decoding file '{file_path}': {e}\n\n")

def write_limited_file_content(summary_file, file_path, limit):
    """Writes a limited snippet of file content or full content if FLAT_MODE is True."""
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            limited_content = []  # Create an empty list to store the lines
            line_count = 0
            for line in f:
                limited_content.append(line)  # Add each line to the list
                line_count += 1
                if line_count >= limit:
                    break  # Stop reading after 'limit' lines

            summary_file.write(
                f"Content (First {len(limited_content)} lines):\n{''.join(limited_content)}\n\n"
            )
    except UnicodeDecodeError as e:
        summary_file.write(f"Error decoding file '{file_path}': {e}\n\n")

def print_summary_from_file(summary_filepath):
    """Prints a formatted summary from the summary file."""
    with open(summary_filepath, "r", encoding="utf-8") as summary_file:
        summary_content = summary_file.read()

    table = Table(title="[bold blue]Summary of Files and Directories[/]", expand=True, width=150)
    table.add_column("File/Directory", style="cyan", no_wrap=False)
    table.add_column("Path", style="magenta", no_wrap=False)

    for line in summary_content.splitlines():
        if "File:" in line:
            file_or_dir, path = extract_file_dir_info(line)
            table.add_row(file_or_dir, path)

    print(table)

    tree_structure = "\n".join(
        line for line in summary_content.splitlines() if "Subdirectory:" in line or "File:" in line
    )
    print(Panel(tree_structure, title="[bold green]Tree Structure[/]", expand=True, width=150))

def extract_file_dir_info(line):
    """Extracts file/directory info from a line."""
    file_or_dir = line.split(":")[1].strip()
    path = line.split("(")[1].strip().split(")")[0] if "(" in line else ""
    return file_or_dir, path

def count_lines_in_file(filepath):
    """Counts the number of lines in a file."""
    with open(filepath, "r", encoding="utf-8") as f:
        return len(f.readlines())

if __name__ == "__main__":
    current_directory = os.getcwd()
    summarize_directory(current_directory, limit=10)  # Set a default limit of 10 lines
