#update_project_table.py
tool_type_for_Tool_Manager = "focus"
import os
import json
import uuid

# Emojis for visual enhancement
TASK_EMOJI = "📄"
SUBTASK_EMOJI = "   └─ "
IN_PROGRESS_EMOJI = "⏳"
COMPLETED_EMOJI = "✅"
FOCUS_EMOJI = "🎯"

ACTIVE_PROJECTS_FILE = os.path.join('..', '..', 'FocusTable', 'active_projects.json')
COMPLETED_PROJECTS_FILE = os.path.join('..', '..', 'FocusTable', 'completed_projects.json')

def update_project_table(
    project_name: str = None,
    task_guid: str = None,
    task_name: str = None,
    goal: str = None,
    description: str = None,
    time_horizon: str = None,
    focus_level: int = None,
    current_focus: int = None,
    status: str = None,
    importance_level: int = None,
    difficulty: int = None,
    completeness: float = None,
    current_cost: float = None,
    result: str = None,
    parent_task_guid: str = None,
) -> dict:
    """
    Updates the project and task data directly in the JSON files.
    Creates the JSON files if they don't exist.
    Moves completed projects to 'completed_projects.json'.

    Args:
        project_name (str, optional): Name of the project to update.
        task_guid (str, optional): Unique identifier for the task. If not provided
            for a new task, one will be generated.
        task_name (str, optional): ... (other parameter descriptions)
        # ... other parameters ...

    Returns:
        dict: A dictionary indicating success or failure and a message.
    """

    try:
        # ---- Check and Create Files if Needed ----
        if not os.path.exists(ACTIVE_PROJECTS_FILE):
            print(f"File '{ACTIVE_PROJECTS_FILE}' not found, creating it...")
            os.makedirs(os.path.dirname(ACTIVE_PROJECTS_FILE), exist_ok=True)
            with open(ACTIVE_PROJECTS_FILE, 'w') as f:
                json.dump({}, f, indent=4)

        if not os.path.exists(COMPLETED_PROJECTS_FILE):
            print(f"File '{COMPLETED_PROJECTS_FILE}' not found, creating it...")
            os.makedirs(os.path.dirname(COMPLETED_PROJECTS_FILE), exist_ok=True)
            with open(COMPLETED_PROJECTS_FILE, 'w') as f:
                json.dump({}, f, indent=4)

        # ---- Load Project Data ----
        with open(ACTIVE_PROJECTS_FILE, 'r') as f:
            active_projects = json.load(f)
        with open(COMPLETED_PROJECTS_FILE, 'r') as f:
            completed_projects = json.load(f)

        # --- Logic for Finding and Updating Projects/Tasks ---
        project = active_projects.get(project_name)
        if not project:
            if project_name:
                print(f"Project '{project_name}' not found. Creating a new project.")
                active_projects[project_name] = {"tasks": []}
                project = active_projects[project_name]
            else:
                return {"status": "failure", "message": "Project name is required."}

        if task_guid:
            target_task = next((t for t in project["tasks"] if t["guid"] == task_guid), None)
        else:
            target_task = None

        if target_task:
            # Update existing task
            for attr, value in locals().items():
                if attr not in ("project_name", "task_guid", "active_projects", "completed_projects", "project", "target_task") \
                        and value is not None:
                    target_task[attr] = value
        else:
            # Add new task
            new_task = {
                "guid": str(uuid.uuid4()) if task_guid is None else task_guid,
                "name": task_name,
                "goal": goal,
                "description": description,
                "time_horizon": time_horizon,
                "focus_level": focus_level,
                "current_focus": current_focus,
                "status": status,
                "importance_level": importance_level,
                "difficulty": difficulty,
                "completeness": completeness,
                "current_cost": current_cost,
                "result": result,
                "parent_task_guid": parent_task_guid
            }
            project["tasks"].append(new_task)

        # ---  Move Completed Projects ---
        for proj_name, proj_data in list(active_projects.items()):
            if all(task.get("completeness", 0) == 1.0 for task in proj_data.get("tasks", [])):
                completed_projects[proj_name] = active_projects.pop(proj_name)

        # ---  Save Updated Projects to JSON Files ---
        with open(ACTIVE_PROJECTS_FILE, 'w') as f:
            json.dump(active_projects, f, indent=4)
        with open(COMPLETED_PROJECTS_FILE, 'w') as f:
            json.dump(completed_projects, f, indent=4)

        return {"status": "success", "message": "Project table updated successfully."}

    except Exception as e:
        return {"status": "failure", "message": f"Error updating project table: {str(e)}"}



update_project_table_description_json = {
    'function_declarations': [
        {
            'name': 'update_project_table',
            'description': 'Updates project and task details in the stored tables. Moves completed projects to a separate file.',
            'parameters': {
                'type_': 'OBJECT',
                'properties': {
                    'project_name': {'type_': 'STRING', 'description': 'Name of the project'},
                    'task_guid': {'type_': 'STRING', 'description': 'Unique identifier for the task. If not provided for a new task, one will be generated.'},
                    'task_name': {'type_': 'STRING', 'description': 'Name of the task'},
                    'goal': {'type_': 'STRING', 'description': 'Goal of the task'},
                    'description': {'type_': 'STRING', 'description': 'Detailed description of the task'},
                    'time_horizon': {'type_': 'STRING', 'description': 'Time horizon for completing the task (e.g., "Short Term", "Long Term")'},
                    'focus_level': {'type_': 'INTEGER', 'description': 'Desired level of focus for the task (e.g., 1-5)'},
                    'current_focus': {'type_': 'INTEGER', 'description': 'Current level of focus on the task'},
                    'status': {'type_': 'STRING', 'description': 'Status of the task (e.g., "To Do", "In Progress", "Completed")'},
                    'importance_level': {'type_': 'INTEGER', 'description': 'Importance of the task (e.g., 1-5)'},
                    'difficulty': {'type_': 'INTEGER', 'description': 'Difficulty level of the task (e.g., 1-5)'},
                    'completeness': {'type_': 'NUMBER', 'description': 'Percentage of task completion (0.0 - 1.0)'},
                    'current_cost': {'type_': 'NUMBER', 'description': 'Current cost incurred for the task'},
                    'result': {'type_': 'STRING', 'description': 'Outcome or result of the task'},
                    'parent_task_guid': {'type_': 'STRING', 'description': 'GUID of the parent task (if any)'}
                },
                'required': ['project_name','task_guid']
            }
        }
    ]
}

update_project_table_description_short_str = "Updates project and task details based on provided arguments. Manages data persistence in JSON files."