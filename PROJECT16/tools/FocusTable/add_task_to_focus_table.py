

import json

tool_type_for_Tool_Manager="reflection"

def add_task_to_focus_table(task_name, focus_type, moscow_category,
                      importance, difficulty, reward, total_work, proposed_action,
                      cost_per_run,
                            work_done=0.0, focus_strength=0.0, frustration=0.0,
                      fatigue=0.0, accumulated_cost=0.0, status="NOT_COMPLETED",
                      learned_knowledge="", important_facts="", current_focus=False,
                      goal="", dependencies=[], deadline=None):

    file_path = "../../Brain_settings/focusTables/focus.json"
    if task_name == None:
        task_name="unnamed"
    try:
        # Load the focus table
        with open(file_path, 'r') as f:
            focus_tree = json.load(f)

        # Add the new task to the focus tree
        focus_tree[task_name] = {
            'focus_type': focus_type,
            'moscow_category': moscow_category,
            'importance': importance,
            'difficulty': difficulty,
            'reward': reward,
            'total_work': total_work,
            'proposed_action': proposed_action,
            'cost_per_run': cost_per_run,
            'work_done': work_done,
            'focus_strength': focus_strength,
            'frustration': frustration,
            'fatigue': fatigue,
            'accumulated_cost': accumulated_cost,
            'status': status,
            'learned_knowledge': learned_knowledge,
            'important_facts': important_facts,
            'current_focus': current_focus,
            'goal': goal,
            'dependencies': dependencies,
            'deadline': deadline
        }

        try:
            with open(file_path, 'w') as f:
                json.dump(focus_tree, f, indent=2)
        except Exception as E:
            print(f"Error writing to file: {E}")
            return None

        print(f"Focus table updated with task: {task_name}")
        return focus_tree +"added  to focus  Table" # Return the entire updated focus table

    except Exception as e:
        print(f"Error updating focus table: {e}")
        return None


add_task_to_focus_table_description_json ={
  "function_declarations": [
    {
      "name": "add_task_to_focus_table",
      "description": "Adds a new task to the focus table.",
      "parameters": {
        "type_": "OBJECT",
        "properties": {
          "task_name": {
            "type_": "STRING",
            "description": "The name of the task to add. If None, defaults to 'unnamed'."
          },
          "focus_type": {
            "type_": "STRING",
            "description": "The type of focus for the task (e.g., 'work', 'personal', 'learning')."
          },
          "moscow_category": {
            "type_": "STRING",
            "description": "The MOSCOW category of the task (e.g., 'Must', 'Should', 'Could', 'Won't')."
          },
          "importance": {
            "type_": "INTEGER",
            "description": "The importance level of the task (e.g., 1-5)."
          },
          "difficulty": {
            "type_": "INTEGER",
            "description": "The difficulty level of the task (e.g., 1-5)."
          },
          "reward": {
            "type_": "INTEGER",
            "description": "The reward for completing the task (e.g., 1-5)."
          },
          "total_work": {
            "type_": "INTEGER",
            "description": "The total estimated work required for the task (in units)."
          },
          "proposed_action": {
            "type_": "STRING",
            "description": "The proposed action or steps to take for the task."
          },
          "cost_per_run": {
            "type_": "NUMBER",
            "description": "The cost (in time, energy, etc.) for each attempt or run of the task."
          },
          "work_done": {
            "type_": "NUMBER",
            "description": "The amount of work already completed on the task (in units). Defaults to 0.0."
          },
          "focus_strength": {
            "type_": "NUMBER",
            "description": "The current level of focus dedicated to the task. Defaults to 0.0."
          },
          "frustration": {
            "type_": "NUMBER",
            "description": "The current level of frustration with the task. Defaults to 0.0."
          },
          "fatigue": {
            "type_": "NUMBER",
            "description": "The current level of fatigue experienced with the task. Defaults to 0.0."
          },
          "accumulated_cost": {
            "type_": "NUMBER",
            "description": "The total cost (in time, energy, etc.) accumulated so far for the task. Defaults to 0.0."
          },
          "status": {
            "type_": "STRING",
            "description": "The current status of the task (e.g., 'NOT_COMPLETED', 'IN_PROGRESS', 'COMPLETED'). Defaults to 'NOT_COMPLETED'."
          },
          "learned_knowledge": {
            "type_": "STRING",
            "description": "Any knowledge learned or insights gained while working on the task. Defaults to empty string."
          },
          "important_facts": {
            "type_": "STRING",
            "description": "Any important facts or details relevant to the task. Defaults to empty string."
          },
          "current_focus": {
            "type_": "BOOLEAN",
            "description": "Whether the task is currently the primary focus. Defaults to False."
          },
          "goal": {
            "type_": "STRING",
            "description": "The specific goal or outcome desired from completing the task. Defaults to empty string."
          },
          "dependencies": {
            "type_": "ARRAY",
            "items": {
              "type_": "STRING",
              "description": "A list of other tasks that this task depends on. Defaults to empty list."
            }
          },
          "deadline": {
            "type_": "STRING",
            "description": "The deadline for completing the task (in YYYY-MM-DD format). Defaults to None."
          }
        },
        "required": [
          "task_name",
          "focus_type",
          "moscow_category",
          "importance",
          "difficulty",
          "reward",
          "total_work",
          "proposed_action",
          "cost_per_run"
        ]
      }
    }
  ]
}


add_task_to_focus_table_description_short_str = "Adds a new task to the focus table."  # Short description
