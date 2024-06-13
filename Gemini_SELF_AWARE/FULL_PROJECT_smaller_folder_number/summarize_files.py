import os

# The name of the summary file
SUMMARY_FILENAME = 'summarisation.txt'

def main():
    # Get the current directory
    current_directory = os.getcwd()

    # Construct the full path to the summary file
    summary_filepath = os.path.join(current_directory, SUMMARY_FILENAME)

    print(f"Creating summary file: '{summary_filepath}'")

    # Open the summary file in write mode (using UTF-8 encoding)
    with open(summary_filepath, 'w', encoding='utf-8') as summary_file:
        # Print a header for the summary
        summary_file.write(f"## Summary of Files and Directories in '{current_directory}'\n\n")

        # Process the current directory and all subdirectories
        _process_all_directories(current_directory, summary_file, 0)

        # Write a clear tree structure at the end
        summary_file.write("\n\n--- Tree Structure ---\n")
        _print_tree_structure(current_directory, summary_file, "")

    print(f"Summary file created successfully: '{summary_filepath}'")

def _process_all_directories(directory, summary_file, level):
    """Processes a directory and all its subdirectories, summarizing file content."""
    for item in os.listdir(directory):
        # Construct the full path to the item
        item_path = os.path.join(directory, item)

        # Indentation for better readability
        indent = "  " * level

        # Ignore the summary file and the script itself
        if item in [SUMMARY_FILENAME, os.path.basename(__file__)]:
            continue

        # If it's a file, write its name and content to the summary file
        if os.path.isfile(item_path):
            summary_file.write(f"{indent}File: {item} ({item_path})\n")  # Include path
            try:
                with open(item_path, 'r', encoding='utf-8') as f:  # Specify UTF-8 encoding
                    # Read the entire file content
                    content = f.read()
                    summary_file.write(f"{indent}Content:\n{indent}{content}\n\n")
            except UnicodeDecodeError as e:
                print(f"Error decoding file '{item_path}': {e}")
                # Handle the error (e.g., skip the file, log the error)

        # If it's a directory, recursively process it
        elif os.path.isdir(item_path):
            # Check for __pycache__ directory *before* processing
            if os.path.basename(item_path) == "__pycache__":  # Skip if it's __pycache__
                continue
            summary_file.write(f"{indent}Directory: {item} ({item_path})\n")  # Include path
            _process_all_directories(item_path, summary_file, level + 1)
            # Increase level for indentation in subdirectories

def _print_tree_structure(directory, summary_file, prefix=""):
    """Prints the tree structure of the directory in a more readable format."""
    for index, item in enumerate(os.listdir(directory)):
        item_path = os.path.join(directory, item)
        if os.path.isdir(item_path):
            # Check for __pycache__ directory *before* printing
            if os.path.basename(item_path) == "__pycache__":
                continue
            summary_file.write(f"{prefix}Folder: '{item}'\n")
            _print_tree_structure(item_path, summary_file, prefix + "  ")
        else:
            # Ignore the summary file and the script itself
            if item in [SUMMARY_FILENAME, os.path.basename(__file__)]:
                continue
            summary_file.write(f"{prefix}File: '{item}'\n")

if __name__ == '__main__':
    main()