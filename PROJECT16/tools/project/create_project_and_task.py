import json
from SelAwareAI_Gemini.PROJECT16 import ProjectTableManager

tool_type_for_Tool_Manager = "action"  # Or "reflection" if you want the AI to suggest projects

def create_project_and_task(project_name: str, description: str, goal: str, task_name: str,
                             task_focus_type: str, task_moscow_category: str,
                             task_importance: int, task_difficulty: int, task_reward: int,
                             task_total_work: float, task_proposed_action: str,
                             task_cost_per_run: float):

    project_table_manager = ProjectTableManager()

    # Create the project
    success_message = project_table_manager.create_project(
        name=project_name, description=description, goal=goal
    )
    print(success_message)

    # Add the task to the project
    success_message = project_table_manager.add_task(
        project_name=project_name,
        name=task_name,
        focus_type=task_focus_type,
        moscow_category=task_moscow_category,
        importance=task_importance,
        difficulty=task_difficulty,
        reward=task_reward,
        total_work=task_total_work,
        proposed_action=task_proposed_action,
        cost_per_run=task_cost_per_run
    )
    print(success_message)

    return f"Project '{project_name}' and task '{task_name}' created successfully!"

create_project_and_task_description_json = {
    "function_declarations": [
        {
            "name": "create_project_and_task",
            "description": "Creates a new project and a task within that project.",
            "parameters": {
                "type_": "OBJECT",
                "properties": {
                    "project_name": {
                        "type_": "STRING",
                        "description": "The name of the new project."
                    },
                    "description": {
                        "type_": "STRING",
                        "description": "The description of the new project."
                    },
                    "goal": {
                        "type_": "STRING",
                        "description": "The goal of the new project."
                    },
                    "task_name": {
                        "type_": "STRING",
                        "description": "The name of the new task within the project."
                    },
                    "task_focus_type": {
                        "type_": "STRING",
                        "description": "The focus type of the new task (e.g., 'work', 'personal', 'learning')."
                    },
                    "task_moscow_category": {
                        "type_": "STRING",
                        "description": "The MOSCOW category of the new task (e.g., 'Must', 'Should', 'Could', 'Won't')."
                    },
                    "task_importance": {
                        "type_": "INTEGER",
                        "description": "The importance level of the new task (e.g., 1-5)."
                    },
                    "task_difficulty": {
                        "type_": "INTEGER",
                        "description": "The difficulty level of the new task (e.g., 1-5)."
                    },
                    "task_reward": {
                        "type_": "INTEGER",
                        "description": "The reward for completing the new task (e.g., 1-5)."
                    },
                    "task_total_work": {
                        "type_": "NUMBER",
                        "description": "The estimated total work for the new task (in units)."
                    },
                    "task_proposed_action": {
                        "type_": "STRING",
                        "description": "The proposed action or steps for the new task."
                    },
                    "task_cost_per_run": {
                        "type_": "NUMBER",
                        "description": "The cost (time, energy) per attempt of the new task."
                    }
                },
                "required": [
                    "project_name",
                    "description",
                    "goal",
                    "task_name",
                    "task_focus_type",
                    "task_moscow_category",
                    "task_importance",
                    "task_difficulty",
                    "task_reward",
                    "task_total_work",
                    "task_proposed_action",
                    "task_cost_per_run"
                ]
            }
        }
    ]
}