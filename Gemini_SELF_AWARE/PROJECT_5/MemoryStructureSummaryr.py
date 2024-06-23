import os
import datetime

def summarize_folder(folder_path, output_file="MemoryStructureSummary.txt"):
    """Summarizes the folder structure and file names within the 'Memories'
       folder and all its subfolders. Saves the summary to a file.

    Args:
      folder_path: The path to the 'Memories' folder.
      output_file: The name of the file to save the summary to.
                   Defaults to "MemoryStructureSummary.txt".
    """

    summary = ""

    for root, dirs, files in os.walk(folder_path):
        # Calculate relative path to the 'Memories' folder
        relative_path = os.path.relpath(root, folder_path)

        # Add "Memories/" prefix
        if relative_path == ".":
            relative_path = "Memories"
        else:
            relative_path = "Memories/" + relative_path

        summary += f"{relative_path}\n"

        # Sort directories and files alphabetically for better readability
        dirs.sort()
        files.sort()

        for dir in dirs:
            summary += f"  - {dir}\n"
        for file in files:
            summary += f"    - {file}\n"

    with open(output_file, "w", encoding='utf-8') as f:
        f.write(summary)

    print(f"Folder structure saved to {output_file}")

# Example usage:
# Assuming the script is in the same directory as the 'Memories' folder
script_dir = os.path.dirname(os.path.abspath(__file__))
memories_folder = os.path.join(script_dir, "Memories")
summarize_folder(memories_folder)