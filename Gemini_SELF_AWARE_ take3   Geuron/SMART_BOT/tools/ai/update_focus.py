tool_type_for_TOOL_MANAGER="all"


update_focus_short_description=""" Updates the focus file with new focus information.. 
        """



import json
import os


# Path to the focus file (adjust if needed)
focus_file_path = '../../focus.json'

def update_focus(new_focus: str, category: str = None, frustration_level: int = None, focus_strength: int = None, defocus_threshold: int = None) -> dict:
  """
  Updates the focus file with new focus information.

  Args:
    new_focus (str): The new focus text to be added to the focus file.
    category (str, optional): The category of the focus (e.g., "Research", "Task", "Goal"). Defaults to None.
    frustration_level (int, optional): A level indicating the current frustration level (0-10). Defaults to None.
    focus_strength (int, optional): A level indicating the strength of the focus (0-10). Defaults to None.
    defocus_threshold (int, optional): A level indicating the threshold at which the focus should be considered defocused (0-10). Defaults to None.

  Returns:
    dict: A dictionary containing the status of the operation, a message, and the updated focus text.
  """

  try:
    # Read the existing focus from the file
    with open(focus_file_path, 'r') as f:
      focus_data = json.load(f)

    # Create a new focus item dictionary
    new_focus_item = {
      "text": new_focus,
      "category": category,
      "frustration_level": frustration_level,
      "focus_strength": focus_strength,
      "defocus_threshold": defocus_threshold
    }

    # Append the new focus item to the existing focus list
    focus_data['focus'].append(new_focus_item)

    # Write the updated focus back to the file
    with open(focus_file_path, 'w') as f:
      json.dump(focus_data, f, indent=4)

    return {
      "status": "success",
      "message": f"Focus updated with: '{new_focus}'",
      "updated_focus": focus_data['focus']
    }

  except Exception as e:
    return {
      "status": "failure",
      "message": f"Error updating focus: {str(e)}"
    }

# Example usage:
# new_focus_text = "My new focus is to learn more about programming."
# result = update_focus(new_focus_text, category="Goal", frustration_level=0, focus_strength=9, defocus_threshold=3)
# print(result)