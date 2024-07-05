import os
import json
from tabulate import tabulate
import uuid

# Emojis for visual enhancement (can be customized)
TASK_EMOJI = "📄"
SUBTASK_EMOJI = "   └─ "
IN_PROGRESS_EMOJI = "⏳"
COMPLETED_EMOJI = "✅"
FOCUS_EMOJI = "🎯"

class Project:
    """Represents a project with tasks and subtasks."""

    def __init__(self, name, description=""):
        self.name = name
        self.description = description
        self.tasks = {}
        self.completed = False

    def add_task(self, task):
        """Adds a task to the project."""
        self.tasks[task.guid] = task

    def get_tasks(self):
        """Returns a list of tasks in the project."""
        return self.tasks.values()

    def is_completed(self):
        """Checks if all tasks in the project are completed."""
        return all(task.completeness == 1.0 for task in self.tasks.values())

    def get_total_cost(self):
        """Calculates the total cost of the project."""
        return sum(task.get_total_cost() for task in self.tasks.values())

    def find_task(self, guid):
        """Finds a task within the project by its GUID."""
        task = self.tasks.get(guid)
        if task:
            return task
        for t in self.tasks.values():
            task = t.find_task(guid)
            if task:
                return task
        return None

class Task:
    """Represents a task with optional subtasks."""

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
        self.completeness = completeness
        self.current_cost = current_cost
        self.result = result
        self.parent = parent
        self.children = []

    def update_focus(self, new_focus):
        """Updates the current focus level of the task."""
        self.current_focus = new_focus

    def update_completeness(self, new_completeness):
        """Updates the completeness of the task."""
        self.completeness = new_completeness

    def update_cost(self, new_cost):
        """Updates the cost of the task."""
        self.current_cost = new_cost

    def update_result(self, result_text):
        """Updates the result of the task."""
        self.result = result_text

    def add_child(self, child):
        """Adds a subtask to the task."""
        self.children.append(child)
        child.parent = self

    def get_total_cost(self):
        """Calculates the total cost of the task, including subtasks."""
        return self.current_cost + sum(child.get_total_cost() for child in self.children)

    def find_task(self, guid):
        """Finds a task (or self) by GUID."""
        if self.guid == guid:
            return self
        for child in self.children:
            found_task = child.find_task(guid)
            if found_task:
                return found_task
        return None

# Dictionaries to store active and completed projects
active_projects = {}
completed_projects = {}

# --- Data Representation, File Output, and Project Management ---

def format_focus(current, target):
    """Formats the focus display with an emoji."""
    return f"{FOCUS_EMOJI} {current}/{target}"

def get_project_data(project):
    """Retrieves project data and formats it for enhanced display."""
    project_data = []
    for task in project.get_tasks():
        parent_name = f"{SUBTASK_EMOJI}{task.parent.name}" if task.parent else ""
        status_emoji = COMPLETED_EMOJI if task.completeness == 1.0 else IN_PROGRESS_EMOJI
        project_data.append([
            parent_name,
            f"{TASK_EMOJI} {task.name}",
            task.goal,
            task.time_horizon,
            format_focus(task.current_focus, task.focus_level),
            f"{status_emoji} {task.status}",
            task.importance_level,
            task.difficulty,
            f"{task.completeness:.0%}",
            f"{task.current_cost:.2f}",
            task.result
        ])
        for child in task.children:
            status_emoji = COMPLETED_EMOJI if child.completeness == 1.0 else IN_PROGRESS_EMOJI
            project_data.append([
                f"{SUBTASK_EMOJI}{task.name}",
                f"   {TASK_EMOJI} {child.name}",
                child.goal,
                child.time_horizon,
                format_focus(child.current_focus, child.focus_level),
                f"{status_emoji} {child.status}",
                child.importance_level,
                child.difficulty,
                f"{child.completeness:.0%}",
                f"{child.current_cost:.2f}",
                child.result
            ])
    return project_data


def project_to_dict(project):
    """Converts a Project object to a dictionary for JSON serialization."""
    return {
        "name": project.name,
        "description": project.description,
        "tasks": [task_to_dict(task) for task in project.get_tasks()],
        "completed": project.completed
    }

def task_to_dict(task):
    """Converts a Task object to a dictionary for JSON serialization."""
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

def save_projects_to_json(projects, filename):
    """Saves project data to a JSON file in the 'FocusTable' folder."""
    folder_name = "FocusTable"
    if not os.path.exists(folder_name):
        os.makedirs(folder_name)

    file_path = os.path.join(folder_name, filename)

    data_to_save = {
        project_name: project_to_dict(project)
        for project_name, project in projects.items()
    }

    with open(file_path, 'w') as f:
        json.dump(data_to_save, f, indent=4)

def move_completed_projects():
    """Moves completed projects to the completed_projects dictionary."""
    for project_name, project in list(active_projects.items()):
        if project.is_completed():
            completed_projects[project_name] = active_projects.pop(project_name)

# --- Example Usage with Multiple Projects ---

# Create Project A
project_a = Project("Project A", "A project to analyze and improve sales strategies.")
task_1 = Task("Task 1", "Complete the sales report",
              description="Generate a comprehensive report on recent sales figures.",
              time_horizon="Short Term", focus_level=4,
              current_focus=3, completeness=1.0, current_cost=15.0,
              result="Sales report generated, showing a 10% increase.")
subtask_1a = Task("Subtask 1a", "Gather data",
                  description="Collect sales data from various sources.",
                  completeness=1.0, current_cost=5.0,
                  result="Data successfully gathered from CRM and sales spreadsheets.",
                  parent=task_1)
subtask_1b = Task("Subtask 1b", "Write the report",
                  description="Compile the data and write the sales report.",
                  completeness=1.0, current_cost=7.0,
                  result="Report drafted, including charts and analysis.",
                  parent=task_1)
subtask_1c = Task("Subtask 1c", "Review the report",
                  description="Review the report for accuracy and clarity.",
                  completeness=1.0, current_cost=3.0,
                  result="Report reviewed and approved by stakeholders.",
                  parent=task_1)
task_1.add_child(subtask_1a)
task_1.add_child(subtask_1b)
task_1.add_child(subtask_1c)

task_2 = Task("Task 2", "Prepare for the presentation",
              description="Create materials and rehearse for the sales presentation.",
              time_horizon="Mid Term", focus_level=3,
              current_focus=2, completeness=1.0, current_cost=10.0,
              result="Presentation prepared with key findings and recommendations.")
subtask_2a = Task("Subtask 2a", "Create slides",
                  description="Design visually appealing presentation slides.",
                  completeness=1.0, current_cost=4.0,
                  result="Slides created with impactful visuals and data.",
                  parent=task_2)
subtask_2b = Task("Subtask 2b", "Rehearse the presentation",
                  description="Practice the presentation delivery.",
                  completeness=1.0, current_cost=6.0,
                  result="Presentation rehearsal completed.",
                  parent=task_2)
task_2.add_child(subtask_2a)
task_2.add_child(subtask_2b)

project_a.add_task(task_1)
project_a.add_task(task_2)

# Create Project B
project_b = Project("Project B", "Develop a new marketing campaign.")
task_b1 = Task("Task B1", "Market Research",
               description="Conduct thorough market research to identify trends.",
               time_horizon="Short Term", focus_level=3,
               current_focus=2, completeness=0.8, current_cost=20.0,
               result="Market research report compiled, identifying key demographics.")
subtask_b1a = Task("Subtask B1a", "Analyze Competitors",
                   description="Analyze competitor strategies and market positioning.",
                   completeness=1.0, current_cost=8.0,
                   result="Competitor analysis completed.",
                   parent=task_b1)
subtask_b1b = Task("Subtask B1b", "Identify Customer Needs",
                   description="Conduct surveys and focus groups to understand customer needs.",
                   completeness=0.7, current_cost=12.0,
                   result="Surveys conducted, data analysis in progress.",
                   parent=task_b1)
task_b1.add_child(subtask_b1a)
task_b1.add_child(subtask_b1b)
project_b.add_task(task_b1)

active_projects["Project A"] = project_a
active_projects["Project B"] = project_b

# --- Example: Update and Manage Projects ---
target_guid_project_b = subtask_b1b.guid
found_task_b = project_b.find_task(target_guid_project_b)
if found_task_b:
    found_task_b.update_completeness(0.9)
    found_task_b.update_result("Data analysis completed, preparing the final report.")

# Move completed projects
move_completed_projects()

# Save projects to JSON files
save_projects_to_json(active_projects, "active_projects.json")
save_projects_to_json(completed_projects, "completed_projects.json")

# --- Example: Display Project Data (using tabulate and emojis) ---
print("Active Projects:")
for project_name, project in active_projects.items():
    print(f"\n--- {project_name} ---")
    print(tabulate(get_project_data(project), headers=[
        "Parent Task", "Task Name", "Goal", "Time Horizon",
        "other", "Status", "Importance", "Difficulty",
        "Completeness", "Cost", "Result"
    ]))

print("\nCompleted Projects:")
for project_name, project in completed_projects.items():
    print(f"\n--- {project_name} ---")
    print(tabulate(get_project_data(project), headers=[
        "Parent Task", "Task Name", "Goal", "Time Horizon",
        "other", "Status", "Importance", "Difficulty",
        "Completeness", "Cost", "Result"
    ]))