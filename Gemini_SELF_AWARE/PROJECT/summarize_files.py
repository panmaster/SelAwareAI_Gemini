import os
from rich import print  # Import Rich library for colorful output
from rich.panel import Panel
from rich.table import Table

# Constants
SUMMARY_FILENAME = 'summarisation.txt'
CONTENT_LIMIT = 500000  # Limit for file content (in lines)
FOLDER_STRUCTURE_LIMIT = 4  # Limit for folder structure (in levels)
CONNECTION_MAP_LIMIT = 10  # Limit for connection map lines in specific files

# Variable for flat mode (include file contents)
flat_mode = True  # Set to True to include file content for specific files


def main():
    current_directory = os.getcwd()
    summary_filepath = os.path.join(current_directory, SUMMARY_FILENAME)

    print(f"[bold blue]Creating summary file: '{summary_filepath}'[/]")

    try:
        with open(summary_filepath, 'w', encoding='utf-8') as summary_file:
            summary_file.write(f"## Summary of Files and Directories in '{current_directory}'\n\n")

            total_lines = _process_all_directories(current_directory, summary_file, 0, current_directory)

        print(f"[bold green]Summary file created successfully: '{summary_filepath}'[/]")
        _print_summary(summary_filepath)

        print(f"[bold yellow]Total number of lines in the summary file: {total_lines}[/]")

    except Exception as e:
        print(f"[bold red]Error creating summary file: {e}[/]")


def _process_all_directories(directory, summary_file, level, root_directory):
    """Processes a directory and all its subdirectories, summarizing file content."""
    total_lines = 0
    try:
        for item in os.listdir(directory):
            item_path = os.path.join(directory, item)
            relative_path = os.path.relpath(item_path, root_directory)
            indent = "  " * level

            # Exclude summarization file and script from summarization
            if item in [SUMMARY_FILENAME, os.path.basename(__file__)]:
                continue

            if os.path.isfile(item_path):
                lines = _write_file_summary(item, relative_path, summary_file, indent)
                total_lines += lines
            elif os.path.isdir(item_path) and os.path.basename(item_path) != "__pycache__":
                summary_file.write(f"{indent}Directory: {item} ({relative_path})\n")
                if level < FOLDER_STRUCTURE_LIMIT:
                    total_lines += _process_all_directories(item_path, summary_file, level + 1, root_directory)

    except Exception as e:
        print(f"[bold red]Error processing directory '{directory}': {e}[/]")
    return total_lines


def _write_file_summary(item, relative_path, summary_file, indent):
    """Writes the summary of a file."""
    try:
        with open(relative_path, 'r', encoding='utf-8') as f:
            content = f.readlines()
            line_count = len(content)
            limited_content = content[:CONTENT_LIMIT]  # Apply content limit

            # Apply CONNECTION_MAP_LIMIT to specific files
            if item in ["MEMORY_initializer.py", "Memory_connecions_map.txt"]:
                limited_content = content[:CONNECTION_MAP_LIMIT]

            summary_file.write(
                f"{indent}File name: {item}\n{indent}Relative path: {relative_path}\n{indent}Number of lines: {line_count}\n")
            if flat_mode and len(limited_content) > 0:
                summary_file.write(
                    f"{indent}Content (First {len(limited_content)} lines):\n{indent}{''.join(limited_content)}\n\n")
            return line_count + 3  # Include 3 lines for file name, path, and line count
    except UnicodeDecodeError as e:
        print(f"[bold red]Error decoding file '{relative_path}': {e}[/]")
        return 0


def _print_summary(summary_filepath):
    """Prints a colorful summary of the content of the summary file."""
    try:
        with open(summary_filepath, 'r', encoding='utf-8') as summary_file:
            summary_content = summary_file.read()

            table = Table(title=f"[bold blue]Summary of Files and Directories[/]", expand=True, width=150)
            table.add_column("File/Directory", style="cyan", no_wrap=False)
            table.add_column("Relative Path", style="magenta", no_wrap=False)
            table.add_column("Number of Lines", style="yellow", no_wrap=False)

            for line in summary_content.splitlines():
                if "File name:" in line:
                    file_name, relative_path, line_count = _extract_file_info(line)
                    table.add_row(file_name, relative_path, line_count)

            print(table)

    except Exception as e:
        print(f"[bold red]Error printing summary: {e}[/]")


def _extract_file_info(line):
    """Extracts file information from a line."""
    parts = line.split("\n")
    file_name = parts[0].split(":")[1].strip()
    relative_path = parts[1].split(":")[1].strip()
    line_count = parts[2].split(":")[1].strip()
    return file_name, relative_path, line_count


if __name__ == '__main__':
    main()