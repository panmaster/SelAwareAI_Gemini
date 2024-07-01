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
                 last_focused: str = None, parent_task: str = None, priority: int = 5):
        self.name = name
        self.focus_type = focus_type
        self.moscow_category = moscow_category
        self.importance = importance
        self.difficulty = difficulty
        self.reward = reward
        self.total_work = total_work
        self.proposed_action = proposed_action
        self.cost_per_run = cost_per_run
        self.work_done = work_done
        self.focus_strength = focus_strength
        self.frustration = frustration
        self.fatigue = fatigue
        self.accumulated_cost = accumulated_cost
        self.status = status
        self.learned_knowledge = learned_knowledge
        self.important_facts = important_facts
        self.current_focus = current_focus
        self.goal = goal
        self.dependencies = dependencies
        self.deadline = deadline
        self.calculated_score = calculated_score
        self.last_focused = last_focused
        self.parent_task = parent_task
        self.priority = priority

class Task(Subtask):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.subtasks: List[Subtask] = []

class Project:
    def __init__(self, name: str, description: str, goal: str,
                 tasks: List[Union[Task, Subtask]] = None,
                 priority: int = 5, deadline: str = None):
        self.name = name
        self.description = description
        self.goal = goal
        self.tasks = tasks if tasks is not None else []
        self.priority = priority
        self.deadline = deadline

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
    def __init__(self, table_file="Brain_settings/ProjectTable/project_table.json"):
        self.table_file = table_file
        self.project_table: Dict[str, Project] = self.load_table()
        self.current_project: Optional[Project] = None

    def load_table(self) -> Dict[str, Project]:
        """Loads the project table from the JSON file."""
        try:
            with open(self.table_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
            return self._convert_to_objects(data)
        except FileNotFoundError:
            print(f"Project table file not found. Creating a new one.")
            return {}

    def _convert_to_objects(self, data: Dict) -> Dict[str, Project]:
        """Converts the loaded JSON data into Project objects."""
        projects = {}
        for project_name, project_data in data.items():
            tasks = []
            for task_data in project_data.get("tasks", []):
                subtasks = [Subtask(**subtask_data) for subtask_data in task_data.get("subtasks", [])]
                task = Task(**task_data, subtasks=subtasks)
                tasks.append(task)
            project = Project(**project_data, tasks=tasks)
            projects[project_name] = project
        return projects

    def save_table(self) -> None:
        """Saves the project table to the JSON file."""
        try:
            data = self._convert_to_dict(self.project_table)
            with open(self.table_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2)
        except Exception as e:
            print(f"Error saving project table: {e}")

    def _convert_to_dict(self, projects: Dict[str, Project]) -> Dict:
        """Converts Project objects to a dictionary for JSON serialization."""
        data = {}
        for project_name, project in projects.items():
            tasks = []
            for task in project.tasks:
                subtasks = [subtask.__dict__ for subtask in task.subtasks]
                tasks.append({**task.__dict__, "subtasks": subtasks})
            data[project_name] = {**project.__dict__, "tasks": tasks}
        return data

    def create_project(self, name: str, description: str, goal: str, priority: int = 5, deadline: str = None) -> str:
        """Creates a new project and adds it to the project table."""
        if name in self.project_table:
            return f"Project '{name}' already exists."
        self.project_table[name] = Project(name, description, goal, priority=priority, deadline=deadline)
        self.save_table()
        return f"Project '{name}' created successfully."

    def add_task(self, project_name: str, **kwargs) -> str:
        """Adds a new task to the specified project."""
        project = self.project_table.get(project_name)
        if not project:
            return f"Project '{project_name}' not found."
        project.tasks.append(Task(**kwargs))
        self.save_table()
        return f"Task '{kwargs.get('name', 'Unnamed Task')}' added to project '{project_name}'."

    def add_subtask(self, project_name: str, task_name: str, **kwargs) -> str:
        """Adds a new subtask to the specified task within a project."""
        project = self.project_table.get(project_name)
        if not project:
            return f"Project '{project_name}' not found."

        task = project.get_task_by_name(task_name)
        if not task:
            return f"Task '{task_name}' not found in project '{project_name}'."

        task.subtasks.append(Subtask(**kwargs, parent_task=task_name))
        self.save_table()
        return f"Subtask '{kwargs.get('name', 'Unnamed Subtask')}' added to task '{task_name}' in project '{project_name}'."

    def get_project(self, project_name: str) -> Optional[Project]:
        """Returns the project object for the given project name."""
        return self.project_table.get(project_name)

    def remove_project(self, project_name: str) -> str:
        """Removes a project from the project table."""
        if project_name in self.project_table:
            del self.project_table[project_name]
            self.save_table()
            return f"Project '{project_name}' removed successfully."
        else:
            return f"Project '{project_name}' not found."

    def update_project(self, project_name: str, **kwargs) -> str:
        """Updates the attributes of a project."""
        project = self.project_table.get(project_name)
        if not project:
            return f"Project '{project_name}' not found."

        for key, value in kwargs.items():
            if hasattr(project, key):
                setattr(project, key, value)

        self.save_table()
        return f"Project '{project_name}' updated successfully."

    def remove_task(self, project_name: str, task_name: str) -> str:
        """Removes a task from the specified project."""
        project = self.project_table.get(project_name)
        if not project:
            return f"Project '{project_name}' not found."

        project.tasks = [task for task in project.tasks if task.name != task_name]
        self.save_table()
        return f"Task '{task_name}' removed from project '{project_name}'."

    def update_task(self, project_name: str, task_name: str, **kwargs) -> str:
        """Updates the attributes of a task within a project."""
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
        """Removes a subtask from a specific task within a project."""
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
        """Updates the attributes of a subtask within a task in a project."""
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

    def get_current_project(self) -> Optional[Project]:
        """Returns the currently active project."""
        return self.current_project

    def set_current_project(self, project: Project) -> None:
        """Sets the currently active project."""
        self.current_project = project

    def get_highest_priority_task(self, project: Optional[Project] = None) -> Optional[Task]:
        """
        Returns the highest priority task from the specified project,
        or the current project if none is specified.
        """
        if project is None:
            project = self.current_project
        if project:
            return project.get_highest_priority_task()
        return None