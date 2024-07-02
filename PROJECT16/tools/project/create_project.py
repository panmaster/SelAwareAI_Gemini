tool_type_for_Tool_Manager = "action"
from typing import List
import json
from SelAwareAI_Gemini.PROJECT16.ProjectTableManager import ProjectTableManager

def create_project(
    name: str,
    description: str,
    goal: str,
    problem_statement: str = None,
    subgoals: List[str] = None,
    predicted_outcome: str = None,
) -> str:
    """
    Creates a new project with name, description, goal, optional problem statement,
    subgoals, and predicted outcome.
    """

    project_table_manager = ProjectTableManager()

    result = project_table_manager.create_project(
        name=name,
        description=description,
        goal=goal,
        problem_statement=problem_statement,
        subgoals=subgoals,
        predicted_outcome=predicted_outcome
    )
    return result

create_project_description_json = {
    "function_declarations": [
        {
            "name": "create_project",
            "description": "Creates a new project to solve a problem, achieve a goals, or gain knowledge by qlearning",
            "parameters": {
                "type_": "OBJECT",
                "properties": {
                    "name": {
                        "type_": "STRING",
                        "description": "The name of the new project."
                    },
                    "description": {
                        "type_": "STRING",
                        "description": "A detailed description of the project."
                    },
                    "goal": {
                        "type_": "STRING",
                        "description": "The ultimate goal or objective of the project."
                    },
                    "problem_statement": {
                        "type_": "STRING",
                        "description": "A clear statement of the problem the project aims to solve."
                    },
                    "subgoals": {
                        "type_": "ARRAY",
                        "items": {"type_": "STRING"},
                        "description": "A list of subgoals that contribute to the main goal."
                    },
                    "predicted_outcome": {
                        "type_": "STRING",
                        "description": "The predicted outcome of the project if successful."
                    }
                },
                "required": [
                    "name",
                    "description",
                    "goal"
                ]
            }
        }
    ]
}

create_project_description_short_str = "Creates a new project."