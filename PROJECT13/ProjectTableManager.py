import json
from typing import List, Dict, Union, Optional


class Subtask:
    def __init__(self, name: str, focus_type: str, moscow_category: str, importance: int,
                 difficulty: int, reward: int, total_work: float, proposed_action: str,
                 cost_per_run: float, work_done: float = 0.0, focus_strength: float = 0.0,
                 frustration: float = 0.0, fatigue: float = 0.0, accumulated_cost: float = 0.0,
                 status: str = "NOT_COMPLETED", learned_knowledge: str = "",
                 important_facts: str = "", current_focus: bool = False, goal: str = "",
                 dependencies: List[str] = [], deadline: str = None, calculated_score: float = 0.0,
                 last_focused: str = None, parent_task: str = None):
        self.name = name
        self.focus_type = focus_type
        self.moscow_category = moscow_category
        self.importance = importance
        self.difficulty = difficulty
        self.reward = reward
        self.total_work = total_work
        self.proposed_action = proposed_action
        self.cost_per_run = cost_per_run
        # ... (Other attributes remain the same) ...
        self.parent_task = parent_task


class Task(Subtask):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.subtasks: List[Subtask] = []


class Project:
    def __init__(self, name: str, description: str, goal: str,
                 tasks: List[Union[Task, Subtask]] = None,
                 priority: int = 5, deadline: str = None):
        # ... (Attributes remain the same) ...
        self.tasks = tasks if tasks is not None else []

    def get_highest_priority_task(self) -> Optional[Task]:
        """Returns the task with the highest priority."""
        if not self.tasks:
            return None
        return sorted(self.tasks, key=lambda task: task.priority, reverse=True)[0]

    def get_task_by_name(self, task_name: str) -> Optional[Task]:
        """Returns a task by its name within the project."""
        for task in self.tasks:
            if task.name == task_name:
                return task
        return None


class ProjectTableManager:
    def __init__(self, table_file="table_file="Brain_settings/Q_tables/q_table.json):
    # ... (Initialization remains the same) ...

    # ... (load_table, _convert_to_objects, save_table,
    #      _convert_to_dict, create_project, add_task,
    #      add_subtask, get_project remain the same) ...

    def remove_project(self, project_name: str) -> str:
        if project_name in self.project_table:
            del self.project_table[project_name]
            self.save_table()
            return f"Project '{project_name}' removed successfully."
        else:
            return f"Project '{project_name}' not found."

    def update_project(self, project_name: str, **kwargs) -> str:
        project = self.project_table.get(project_name)
        if not project:
            return f"Project '{project_name}' not found."

        for key, value in kwargs.items():
            if hasattr(project, key):
                setattr(project, key, value)

        self.save_table()
        return f"Project '{project_name}' updated successfully."

    def remove_task(self, project_name: str, task_name: str) -> str:
        project = self.project_table.get(project_name)
        if not project:
            return f"Project '{project_name}' not found."

        project.tasks = [task for task in project.tasks if task.name != task_name]
        self.save_table()
        return f"Task '{task_name}' removed from project '{project_name}'."

    def update_task(self, project_name: str, task_name: str, **kwargs) -> str:
        project = self.project_table.get(project_name)
        if not project:
            return f"Project '{project_name}' not found."

        task = project.get_task_by_name(task_name)
        if not task:
            return f"Task '{task_name}' not found in project '{project_name}'."

        for key, value in kwargs.items():
            if hasattr(task, key):
                setattr(task, key, value)

        self.save_table()
        return f"Task '{task_name}' in project '{project_name}' updated successfully."

    def remove_subtask(self, project_name: str, task_name: str, subtask_name: str) -> str:
        project = self.project_table.get(project_name)
        if not project:
            return f"Project '{project_name}' not found."

        task = project.get_task_by_name(task_name)
        if not task:
            return f"Task '{task_name}' not found in project '{project_name}'."

        task.subtasks = [subtask for subtask in task.subtasks if subtask.name != subtask_name]
        self.save_table()
        return f"Subtask '{subtask_name}' removed from task '{task_name}' in project '{project_name}'."

    def update_subtask(self, project_name: str, task_name: str, subtask_name: str, **kwargs) -> str:
        project = self.project_table.get(project_name)
        if not project:
            return f"Project '{project_name}' not found."

        task = project.get_task_by_name(task_name)
        if not task:
            return f"Task '{task_name}' not found in project '{project_name}'."

        subtask = next((s for s in task.subtasks if s.name == subtask_name), None)
        if not subtask:
            return f"Subtask '{subtask_name}' not found in task '{task_name}' in project '{project_name}'."

        for key, value in kwargs.items():
            if hasattr(subtask, key):
                setattr(subtask, key, value)

        self.save_table()
        return f"Subtask '{subtask_name}' in task '{task_name}' in project '{project_name}' updated successfully."

    def get_project_status(self, project_name: str) -> Optional[Dict[str, Union[str, int, float]]]:
        """Returns a dictionary with the status of a project."""
        project = self.project_table.get(project_name)
        if not project:
            return None

        total_tasks = len(project.tasks)
        completed_tasks = sum(1 for task in project.tasks if task.status == "COMPLETED")
        progress = (completed_tasks / total_tasks) * 100 if total_tasks > 0 else 0

        status = {
            "name": project.name,
            "description": project.description,
            "goal": project.goal,
            "priority": project.priority,
            "deadline": project.deadline,
            "total_tasks": total_tasks,
            "completed_tasks": completed_tasks,
            "progress": progress
        }
        return status