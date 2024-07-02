tool_type_for_Tool_Manager = "reflection"
import json
import  os
def update_focus_table(task_name: str, focus_type: str = None, moscow_category: str = None,
                      importance: int = None, difficulty: int = None, reward: int = None,
                      total_work: float = None, proposed_action: str = None, cost_per_run: float = None,
                      work_done: float = None, focus_strength: float = None, frustration: float = None,
                      fatigue: float = None, accumulated_cost: float = None, status: str = None,
                      learned_knowledge: str = None, important_facts: str = None, current_focus: bool = None,
                      goal: str = None, dependencies: list = None, deadline: str = None) -> str:
    """
    Updates a task in the focus table.

    Args:
        task_name (str): The name of the task to update.
        focus_type (str, optional): The type of focus for the task (e.g., 'work', 'personal', 'learning').
        moscow_category (str, optional): The MOSCOW category of the task (e.g., 'Must', 'Should', 'Could', 'Won't').
        importance (int, optional): The importance level of the task (e.g., 1-5).
        difficulty (int, optional): The difficulty level of the task (e.g., 1-5).
        reward (int, optional): The reward for completing the task (e.g., 1-5).
        total_work (float, optional): The total estimated work required for the task (in units).
        proposed_action (str, optional): The proposed action or steps to take for the task.
        cost_per_run (float, optional): The cost (in time, energy, etc.) for each attempt or run of the task.
        work_done (float, optional): The amount of work already completed on the task (in units).
        focus_strength (float, optional): The current level of focus dedicated to the task.
        frustration (float, optional): The current level of frustration with the task.
        fatigue (float, optional): The current level of fatigue experienced with the task.
        accumulated_cost (float, optional): The total cost (in time, energy, etc.) accumulated so far for the task.
        status (str, optional): The current status of the task (e.g., 'NOT_COMPLETED', 'IN_PROGRESS', 'COMPLETED').
        learned_knowledge (str, optional): Any knowledge learned or insights gained while working on the task.
        important_facts (str, optional): Any important facts or details relevant to the task.
        current_focus (bool, optional): Whether the task is currently the primary focus.
        goal (str, optional): The specific goal or outcome desired from completing the task.
        dependencies (list, optional): A list of other tasks that this task depends on.
        deadline (str, optional): The deadline for completing the task (in YYYY-MM-DD format).

    Returns:
        str: A message indicating success or failure.
    """
    file_path = "../../Brain_settings/focusTables/focus.json"  # Adjust path as needed

    try:
        with open(file_path, 'r') as f:
            focus_table = json.load(f)

        if task_name not in focus_table:
            return f"Task '{task_name}' not found in the focus table."

        task = focus_table[task_name]  # Access the task by its name

        # Update only the provided parameters
        if focus_type is not None:
            task['focus_type'] = focus_type
        if moscow_category is not None:
            task['moscow_category'] = moscow_category
        if importance is not None:
            task['importance'] = importance
        if difficulty is not None:
            task['difficulty'] = difficulty
        if reward is not None:
            task['reward'] = reward
        if total_work is not None:
            task['total_work'] = total_work
        if proposed_action is not None:
            task['proposed_action'] = proposed_action
        if cost_per_run is not None:
            task['cost_per_run'] = cost_per_run
        if work_done is not None:
            task['work_done'] = work_done
        if focus_strength is not None:
            task['focus_strength'] = focus_strength
        if frustration is not None:
            task['frustration'] = frustration
        if fatigue is not None:
            task['fatigue'] = fatigue
        if accumulated_cost is not None:
            task['accumulated_cost'] = accumulated_cost
        if status is not None:
            task['status'] = status
        if learned_knowledge is not None:
            task['learned_knowledge'] = learned_knowledge
        if important_facts is not None:
            task['important_facts'] = important_facts
        if current_focus is not None:
            task['current_focus'] = current_focus
        if goal is not None:
            task['goal'] = goal
        if dependencies is not None:
            task['dependencies'] = dependencies
        if deadline is not None:
            task['deadline'] = deadline

        with open(file_path, 'w') as f:
            json.dump(focus_table, f, indent=2)

        return f"Task '{task_name}' updated in the focus table."

    except Exception as e:
        return f"Error updating focus table: {e}"

update_focus_table_description_json = {
  "function_declarations": [
    {
      "name": "update_focus_table",
      "description": "Updates a task in the focus table.",
      "parameters": {
        "type_": "OBJECT",
        "properties": {
          "task_name": {
            "type_": "STRING",
            "description": "The name of the task to update."
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
            "type_": "NUMBER",
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
            "description": "The amount of work already completed on the task (in units)."
          },
          "focus_strength": {
            "type_": "NUMBER",
            "description": "The current level of focus dedicated to the task."
          },
          "frustration": {
            "type_": "NUMBER",
            "description": "The current level of frustration with the task."
          },
          "fatigue": {
            "type_": "NUMBER",
            "description": "The current level of fatigue experienced with the task."
          },
          "accumulated_cost": {
            "type_": "NUMBER",
            "description": "The total cost (in time, energy, etc.) accumulated so far for the task."
          },
          "status": {
            "type_": "STRING",
            "description": "The current status of the task (e.g., 'NOT_COMPLETED', 'IN_PROGRESS', 'COMPLETED')."
          },
          "learned_knowledge": {
            "type_": "STRING",
            "description": "Any knowledge learned or insights gained while working on the task."
          },
          "important_facts": {
            "type_": "STRING",
            "description": "Any important facts or details relevant to the task."
          },
          "current_focus": {
            "type_": "BOOLEAN",
            "description": "Whether the task is currently the primary focus."
          },
          "goal": {
            "type_": "STRING",
            "description": "The specific goal or outcome desired from completing the task."
          },
          "dependencies": {
            "type_": "ARRAY",
            "items": {
              "type_": "STRING",
              "description": "A list of other tasks that this task depends on."
            }
          },
          "deadline": {
            "type_": "STRING",
            "description": "The deadline for completing the task (in YYYY-MM-DD format)."
          }
        },
        "required": ["task_name"]
      }
    }
  ]
}

update_focus_table_description_short_str = "Updates a task in the focus table."

def check_update_focus_table():
    """
    Function to check if the update_focus_table function works correctly.
    """
    file_path = os.path.abspath("../../Brain_settings/focusTables/focus.json")

    # 1. Load the focus table:
    try:
        with open(file_path, 'r') as f:
            focus_table = json.load(f)
        print(f"Focus table loaded successfully: {focus_table}")
    except FileNotFoundError:
        print(f"Error: Focus table file '{file_path}' not found. Creating a new focus table with example data.")
        focus_table = {
            "Task1": {
                "focus_type": "work",
                "moscow_category": "Must",
                "importance": 5,
                "difficulty": 3,
                "reward": 4,
                "total_work": 10.0,
                "proposed_action": "Write code for the feature",
                "cost_per_run": 1.0,
                "work_done": 0.0,
                "focus_strength": 0.0,
                "frustration": 0.0,
                "fatigue": 0.0,
                "accumulated_cost": 0.0,
                "status": "NOT_COMPLETED",
                "learned_knowledge": "",
                "important_facts": "",
                "current_focus": False,
                "goal": "Finish the feature",
                "dependencies": [],
                "deadline": "2024-07-15"
            },
            "Task2": {
                # ...  add more example tasks here
            }
        }
        with open(file_path, 'w') as f:
            json.dump(focus_table, f, indent=2)

    # 2. Update a task:
    task_to_update = "Task1"
    updated_status = "IN_PROGRESS"
    result = update_focus_table(task_name=task_to_update, status=updated_status)
    print(f"Update result: {result}")

    # 3. Verify the update:
    try:
        with open(file_path, 'r') as f:
            updated_focus_table = json.load(f)
        print(f"Updated focus table: {updated_focus_table}")

        # Access the updated task directly by name
        if updated_focus_table[task_to_update]['status'] == updated_status:
            print(f"Verification: Task '{task_to_update}' updated correctly with status '{updated_status}'")
        else:
            print(f"Verification failed: Task '{task_to_update}' status is not '{updated_status}'")

    except FileNotFoundError:
        print(f"Error: Focus table file '{file_path}' not found after update. ")
    except Exception as e:
        print(f"Error verifying update: {e}")

if __name__ == "__main__":
    check_update_focus_table()