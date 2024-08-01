import os
from rich.tree import Tree
from rich.console import Console

SUMMARY_FILENAME = "summarisation.txt"
console = Console(record=True)

def summarize_directory(directory, summary_file):
    """Recursively summarizes a directory and its contents.

    Args:
        directory (str): The path to the directory to summarize.
        summary_file (TextIOWrapper): The file object to write the summary to.
    """

    # 1. Build and print the tree structure first
    tree = Tree(f"[bold blue]{directory}[/]")
    build_directory_tree(tree, directory)  # Separate function to build tree
    console.print(tree, style="dim")
    summary_file.write(console.export_text())
    summary_file.write("\n\n")

    # 2. Then, write file contents
    write_file_contents(directory, summary_file)

def build_directory_tree(tree, directory):
    """Recursively builds the tree structure."""
    for item in os.listdir(directory):
        item_path = os.path.join(directory, item)
        if item in ("__pycache__", SUMMARY_FILENAME, "summarize_files.py"):
            continue
        if os.path.isdir(item_path):
            sub_tree = tree.add(f"[bold cyan]{item}/[/]")
            build_directory_tree(sub_tree, item_path)
        else:
            tree.add(item)

def write_file_contents(directory, summary_file):
    """Iterates through files and writes content to the summary file."""
    for item in os.listdir(directory):
        item_path = os.path.join(directory, item)
        if item in ("__pycache__", SUMMARY_FILENAME, "summarize_files.py"):
            continue
        if os.path.isfile(item_path):
            write_file_content(summary_file, directory, item, item_path)

def write_file_content(summary_file, directory, filename, file_path):
    """Writes the content of a single file to the summary file."""
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()
        summary_file.write(f"## File: {filename} (in: {directory})\n")
        summary_file.write(content)
        summary_file.write("\n\n")
    except UnicodeDecodeError:
        summary_file.write(f"## File: {filename} (in: {directory})\n")
        summary_file.write("[Could not decode file content]\n\n")

if __name__ == "__main__":
    current_directory = os.getcwd()
    with open(SUMMARY_FILENAME, "w", encoding="utf-8") as f:
        summarize_directory(current_directory, f)
    print(f"[green]Directory summarized to '{SUMMARY_FILENAME}'[/]")