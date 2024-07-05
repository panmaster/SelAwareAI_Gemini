import os
import json
from tabulate import tabulate
import uuid

# Emojis for visual enhancement
TASK_EMOJI = "📄"
SUBTASK_EMOJI = "   └─ "
IN_PROGRESS_EMOJI = "⏳"
COMPLETED_EMOJI = "✅"
FOCUS_EMOJI = "🎯"


class Project:
    def __init__(self, name, description=""):
        self.name = name
        self.description = description
        self.tasks = {}
        self.completed = False

    def to_dict(self):
        return {
            "name": self.name,
            "description": self.description,
            "tasks": [self.task_to_dict(task) for task in self.tasks.values()],
            "completed": self.completed
        }

    def add_task(self, task):
        self.tasks[task.guid] = task

    def get_tasks(self):
        return list(self.tasks.values())

    def is_completed(self):
        return all(task.get_completeness() == 1.0 for task in self.tasks.values())

    def get_total_cost(self):
        return sum(task.get_total_cost() for task in self.tasks.values())

    def find_task(self, guid):
        task = self.tasks.get(guid)
        if task:
            return task
        for t in self.tasks.values():
            task = t.find_task(guid)
            if task:
                return task
        return None

    def task_to_dict(self, task):
        return {
            "guid": task.guid,
            "name": task.name,
            "goal": task.goal,
            "description": task.description,
            "time_horizon": task.time_horizon,
            "focus_level": task.focus_level,
            "current_focus": task.current_focus,
            "status": task.status,
            "importance_level": task.importance_level,
            "difficulty": task.difficulty,
            "completeness": task.completeness,
            "current_cost": task.current_cost,
            "result": task.result,
            "parent": task.parent.guid if task.parent else None,
            "children": [child.guid for child in task.children]
        }


class Task:
    def __init__(self, name, goal, description="", time_horizon="Short Term",
                 focus_level=3, current_focus=0, status="To Do",
                 importance_level=1, difficulty=1, completeness=0.0,
                 current_cost=0.0, result="", parent=None):
        self.guid = str(uuid.uuid4())
        self.name = name
        self.goal = goal
        self.description = description
        self.time_horizon = time_horizon
        self.focus_level = focus_level
        self.current_focus = current_focus
        self.status = status
        self.importance_level = importance_level
        self.difficulty = difficulty
        self.completeness = float(completeness) if completeness is not None else 0.0
        self.current_cost = float(current_cost) if current_cost is not None else 0.0
        self.result = result
        self.parent = parent
        self.children = []

    def get_current_cost(self):
        return self.current_cost if self.current_cost is not None else 0.0

    def get_completeness(self):
        return self.completeness if self.completeness is not None else 0.0

    def get_total_cost(self):
        return self.get_current_cost() + sum(child.get_total_cost() for child in self.children)

    def find_task(self, guid):
        if self.guid == guid:
            return self
        for child in self.children:
            found_task = child.find_task(guid)
            if found_task:
                return found_task
        return None

    def add_child(self, child):
        self.children.append(child)
        child.parent = self


class ProjectManager:
    def __init__(self):
        self.active_projects = self.load_projects_from_json('active_projects.json')
        self.completed_projects = self.load_projects_from_json('completed_projects.json')

    def load_projects_from_json(self, filename):
        folder_name = "FocusTable"
        file_path = os.path.join(folder_name, filename)
        projects = {}
        if os.path.exists(file_path):
            with open(file_path, 'r') as f:
                data = json.load(f)
                for project_name, project_data in data.items():
                    project = Project(project_data["name"], project_data.get("description", ""))
                    projects[project_name] = project

                    task_objects = {}
                    for task_data in project_data.get("tasks", []):
                        task = Task(
                            task_data["name"],
                            task_data["goal"],
                            task_data.get("description", ""),
                            task_data.get("time_horizon", "Short Term"),
                            task_data.get("focus_level", 3),
                            task_data.get("current_focus", 0),
                            task_data.get("status", "To Do"),
                            task_data.get("importance_level", 1),
                            task_data.get("difficulty", 1),
                            task_data.get("completeness", 0.0),
                            task_data.get("current_cost", 0.0),
                            task_data.get("result", ""),
                        )
                        task_objects[task_data["guid"]] = task

                    for task_data in project_data.get("tasks", []):
                        task = task_objects[task_data["guid"]]
                        parent_guid = task_data.get("parent")
                        if parent_guid:
                            parent_task = task_objects.get(parent_guid)
                            if parent_task:
                                parent_task.add_child(task)
                        else:
                            project.add_task(task)

        return projects

    def save_projects_to_json(self, projects, filename):
        folder_name = "FocusTable"
        if not os.path.exists(folder_name):
            os.makedirs(folder_name)

        file_path = os.path.join(folder_name, filename)

        data_to_save = {
            project_name: self.project_to_dict(project)
            for project_name, project in projects.items()
        }

        with open(file_path, 'w') as f:
            json.dump(data_to_save, f, indent=4)

    def format_focus(self, current, target):
        return f"{FOCUS_EMOJI} {current}/{target}"

    def get_project_data(self, project):
        project_data = []
        for task in project.get_tasks():
            parent_name = f"{SUBTASK_EMOJI}{task.parent.name}" if task.parent else ""
            status_emoji = COMPLETED_EMOJI if task.get_completeness() == 1.0 else IN_PROGRESS_EMOJI
            project_data.append([
                parent_name,
                f"{TASK_EMOJI} {task.name}",
                task.goal,
                task.time_horizon,
                self.format_focus(task.current_focus, task.focus_level),
                f"{status_emoji} {task.status}",
                task.importance_level,
                task.difficulty,
                f"{task.get_completeness():.0%}",
                f"{task.get_current_cost():.2f}",
                task.result
            ])
            for child in task.children:
                status_emoji = COMPLETED_EMOJI if child.get_completeness() == 1.0 else IN_PROGRESS_EMOJI
                project_data.append([
                    f"{SUBTASK_EMOJI}{task.name}",
                    f"   {TASK_EMOJI} {child.name}",
                    child.goal,
                    child.time_horizon,
                    self.format_focus(child.current_focus, child.focus_level),
                    f"{status_emoji} {child.status}",
                    child.importance_level,
                    child.difficulty,
                    f"{child.get_completeness():.0%}",
                    f"{child.get_current_cost():.2f}",
                    child.result
                ])
        return project_data

    def project_to_dict(self, project):
        return {
            "name": project.name,
            "description": project.description,
            "tasks": [self.task_to_dict(task) for task in project.get_tasks()],
            "completed": project.completed
        }

    def update_task(self, project_name, task_guid, **kwargs):
        """Updates a task's attributes in a project."""
        project = self.active_projects.get(project_name)
        if project:
            task = project.find_task(task_guid)
            if task:
                for key, value in kwargs.items():
                    if hasattr(task, key):
                        setattr(task, key, value)
                self.save_projects_to_json(self.active_projects, 'active_projects.json')
                return True
        return False

    def get_project(self, project_name):
        """Returns a project by name."""
        return self.active_projects.get(project_name)