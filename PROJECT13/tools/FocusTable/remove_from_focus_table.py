import  json
tool_type_for_Tool_Manager="reflection"
def remove_from_focus_table(task_name):
    file_path = "../../Brain_settings/focusTables/focus.json"  # Adjust path as needed
    """
    Removes a task from the focus table.

    Args:
        task_name (str): The name of the task to remove.

    Returns:
        str: A message indicating success or failure.
    """
    try:
        # Load the focus table
        with open(file_path, 'r') as f:
            focus_tree = json.load(f)

        # Remove the task from the focus tree
        if task_name in focus_tree:
            del focus_tree[task_name]
            # Save the updated focus table
            with open(file_path, 'w') as f:
                json.dump(focus_tree, f, indent=2)
            print(f"Focus table updated. Task '{task_name}' removed.")
            return "Task removed from Focus table"
        else:
            print(f"Task '{task_name}' not found in the focus table.")
            return "Task not found in Focus table"

    except Exception as e:
        print(f"Error removing task from focus table: {e}")
        return "Error removing task from Focus table"

remove_from_focus_table_description_json = {  # JSON description
    "function_declarations": [
        {
            "name": "remove_from_focus_table",
            "description": "Removes a task from the focus table.",
            "parameters": {
                "type_": "OBJECT",
                "properties": {
                    "task_name": {"type_": "STRING", "description": "The name of the task to remove."}
                },

            }
        }
    ]
}

remove_from_focus_table_description_short_str = "Removes a task from the focus table."  # Short