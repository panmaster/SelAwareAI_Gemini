class ProjectManager:
    def __init__(self):
        self.projects = []

    def add_project(self, project):
        self.projects.append(project)

    def get_project(self, name):
        return next((p for p in self.projects if p.name == name), None)

class Project:
    def __init__(self, name):
        self.name = name
        self.tasks = []

    def add_task(self, task):
        self.tasks.append(task)

    def get_task(self, name):
        return next((t for t in self.tasks if t.name == name), None)

class Task:
    def __init__(self, name):
        self.name = name
        self.status = "in progress"

    def set_status(self, status):
        self.status = status

# Example usage
project_manager = ProjectManager()
project = Project("My Project")
project_manager.add_project(project)
task = Task("My Task")
project.add_task(task)
task.set_status("completed")