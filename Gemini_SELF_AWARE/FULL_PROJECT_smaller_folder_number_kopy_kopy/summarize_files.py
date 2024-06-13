import os
from rich import print  # Import Rich library for colorful output
from rich.panel import Panel
from rich.table import Table

# Constants
SUMMARY_FILENAME = 'summarisation.txt'
CONTENT_LIMIT = 500000  # Limit for file content (in lines)
FOLDER_STRUCTURE_LIMIT = 20  # Limit for folder structure (in levels)
CONNECTION_MAP_LIMIT = 20  # Limit for connection map lines

# Variable for flat mode (include file contents)
flat_mode = True  # Set to True to include file content for specific files


def main():
    current_directory = os.getcwd()
    summary_filepath = os.path.join(current_directory, SUMMARY_FILENAME)

    print(f"[bold blue]Creating summary file: '{summary_filepath}'[/]")

    try:
        with open(summary_filepath, 'w', encoding='utf-8') as summary_file:
            summary_file.write(f"## Summary of Files and Directories in '{current_directory}'\n\n")

            total_lines = _process_all_directories(current_directory, summary_file, 0)
            summary_file.write("\n\n--- Tree Structure ---\n")
            _print_tree_structure(current_directory, summary_file, "")
            total_lines += _process_specific_files(current_directory, summary_file, 0)

        print(f"[bold green]Summary file created successfully: '{summary_filepath}'[/]")
        _print_summary(summary_filepath)

        print(f"[bold yellow]Total number of lines in the summary file: {total_lines}[/]")

    except Exception as e:
        print(f"[bold red]Error creating summary file: {e}[/]")


def _process_all_directories(directory, summary_file, level):
    """Processes a directory and all its subdirectories, summarizing file content."""
    total_lines = 0
    try:
        for item in os.listdir(directory):
            item_path = os.path.join(directory, item)
            indent = "  " * level

            if item in [SUMMARY_FILENAME, os.path.basename(__file__)]:
                continue

            if os.path.isfile(item_path):
                lines = _write_file_summary(item, item_path, summary_file, indent)
                total_lines += lines
            elif os.path.isdir(item_path) and os.path.basename(item_path) != "__pycache__":
                summary_file.write(f"{indent}Directory: {item} ({item_path})\n")
                if level < FOLDER_STRUCTURE_LIMIT:
                    total_lines += _process_all_directories(item_path, summary_file, level + 1)

    except Exception as e:
        print(f"[bold red]Error processing directory '{directory}': {e}[/]")
    return total_lines


def _write_file_summary(item, item_path, summary_file, indent):
    """Writes the summary of a file."""
    summary_file.write(f"{indent}File: {item} ({item_path})\n")
    try:
        with open(item_path, 'r', encoding='utf-8') as f:
            content = f.readlines()
            limited_content = content[:CONTENT_LIMIT]  # Apply content limit
            summary_file.write(f"{indent}Content (First {len(limited_content)} lines):\n{indent}{''.join(limited_content)}\n\n")
            return len(limited_content)
    except UnicodeDecodeError as e:
        print(f"[bold red]Error decoding file '{item_path}': {e}[/]")
        return 0


def _print_tree_structure(directory, summary_file, prefix=""):
    """Prints the tree structure of the directory in a more readable format."""
    try:
        for index, item in enumerate(os.listdir(directory)):
            item_path = os.path.join(directory, item)
            if os.path.isdir(item_path) and os.path.basename(item_path) != "__pycache__":
                summary_file.write(f"{prefix}Folder: '{item}'\n")
                if len(prefix) < FOLDER_STRUCTURE_LIMIT * 2:
                    _print_tree_structure(item_path, summary_file, prefix + "  ")
            elif item not in [SUMMARY_FILENAME, os.path.basename(__file__)]:
                summary_file.write(f"{prefix}File: '{item}'\n")

    except Exception as e:
        print(f"[bold red]Error printing tree structure for '{directory}': {e}[/]")


def _process_specific_files(directory, summary_file, level):
    """Processes the 'MEMORY_initializer.py' and 'Memory_connecions_map.txt' files."""
    total_lines = 0
    try:
        for item in os.listdir(directory):
            item_path = os.path.join(directory, item)
            indent = "  " * level

            if item == "MEMORY_initializer.py":
                lines = _write_limited_file_summary(item, item_path, summary_file, indent, CONNECTION_MAP_LIMIT if flat_mode else 0)
                total_lines += lines
            elif item == "Memory_connecions_map.txt":
                lines = _write_limited_file_summary(item, item_path, summary_file, indent, CONNECTION_MAP_LIMIT if flat_mode else 0)
                total_lines += lines

    except Exception as e:
        print(f"[bold red]Error processing specific files in '{directory}': {e}[/]")
    return total_lines


def _write_limited_file_summary(item, item_path, summary_file, indent, limit):
    """Writes the summary of a file with a specified line limit."""
    summary_file.write(f"{indent}File: {item} ({item_path})\n")
    if limit == 0:
        return 2  # Return 2 lines for file name and path only

    try:
        with open(item_path, 'r', encoding='utf-8') as f:
            content = f.readlines()
            limited_content = content[:limit]  # Apply content limit
            summary_file.write(f"{indent}Content (First {len(limited_content)} lines):\n{indent}{''.join(limited_content)}\n\n")
            return len(limited_content) + 2  # Include the two lines for file name and path
    except UnicodeDecodeError as e:
        print(f"[bold red]Error decoding file '{item_path}': {e}[/]")
        return 2


def _print_summary(summary_filepath):
    """Prints a colorful summary of the content of the summary file."""
    try:
        with open(summary_filepath, 'r', encoding='utf-8') as summary_file:
            summary_content = summary_file.read()

            table = Table(title=f"[bold blue]Summary of Files and Directories[/]", expand=True, width=150)
            table.add_column("File/Directory", style="cyan", no_wrap=False)
            table.add_column("Path", style="magenta", no_wrap=False)

            for line in summary_content.splitlines():
                if "File:" in line or "Directory:" in line:
                    file_or_dir, path = _extract_file_or_directory_info(line)
                    table.add_row(file_or_dir, path)

            print(table)

            tree_lines = [line for line in summary_content.splitlines() if "Folder:" in line or "File:" in line]
            tree_structure = "\n".join(tree_lines)
            print(Panel(tree_structure, title="[bold green]Tree Structure[/]", expand=True, width=150))

    except Exception as e:
        print(f"[bold red]Error printing summary: {e}[/]")


def _extract_file_or_directory_info(line):
    """Extracts file or directory information from a line."""
    file_or_dir = line.split(":")[1].strip()
    path = line.split("(")[1].strip().split(")")[0] if "(" in line else ""
    return file_or_dir, path


if __name__ == '__main__':
    main()
