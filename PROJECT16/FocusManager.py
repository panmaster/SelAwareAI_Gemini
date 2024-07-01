#FocusManager.py
import json
import datetime
import  os
from typing import List, Optional, Dict  , Any
from prettytable import PrettyTable  # Import PrettyTable

class Task:
    def __init__(self, name: str, focus_type: str, moscow_category: str, importance: int,
                 difficulty: int, reward: int, total_work: float, proposed_action: str,
                 cost_per_run: float, work_done: float = 0.0, focus_strength: float = 0.0,
                 frustration: float = 0.0, fatigue: float = 0.0, accumulated_cost: float = 0.0,
                 status: str = "NOT_COMPLETED", learned_knowledge: str = "",
                 important_facts: str = "", current_focus: bool = False, goal: str = "",
                 dependencies: List[str] = [], deadline: str = None, calculated_score: float = 0.0,
                 last_focused: datetime.datetime = None):
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


class FocusManager:
    def __init__(self,
                 file_path: str = "C:\Users\DELL\Desktop\selfawareGemini\SelAwareAI_Gemini\PROJECT16\Brain_settings\focusTables\focus.json"):

        self.file_path = file_path

        # Check if the focus file exists, and create it if it doesn't
        if not os.path.exists(self.file_path):
            print(f"Error: File '{self.file_path}' not found. Creating a new focus table.")
            self.create_base_focus_table()

        # Now load the focus table (which should exist now)
        self.focus_table: List[Task] = self.load_focus_table()
        self.last_focus_type = None
        self.consecutive_difficult_tasks = 0

    def calculate_score(self, task: Task, emotions: Dict[str, int] = None, resources: Dict[str, float] = None) -> float:
        score = 0  # Initialize score

        # Base score calculation (adjust weights as needed)
        score += task.importance * 0.5
        score -= task.difficulty * 0.2
        score += task.reward * 0.3

        # Time-based urgency
        if task.last_focused:
            time_since_last_focus = (datetime.datetime.now() - task.last_focused).total_seconds() / 3600
            score += min(time_since_last_focus * 0.1, 5)  # Cap at +5 points

        # Resource management
        if resources:
            if task.energy_required > resources.get('energy', 0):
                score -= 10  # Significant penalty if not enough energy

        # Context switching optimization
        if self.last_focus_type == task.focus_type:
            score += 2  # Bonus for maintaining focus type

        # Balanced workload
        if task.difficulty < 3 and self.consecutive_difficult_tasks > 3:
            score += 5  # Prioritize an easier task after several difficult ones

        return score

    def update_focus_stats(self, task: Task):
        task.last_focused = datetime.datetime.now()
        if task.difficulty > 7:
            self.consecutive_difficult_tasks += 1
        else:
            self.consecutive_difficult_tasks = 0
        self.last_focus_type = task.focus_type

    def load_focus_table(self) -> List[Task]:
        """Loads the focus table from the JSON file. Creates a new one if it doesn't exist."""
        try:
            with open(self.file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            return [Task(**task_data) for task_data in data]
        except FileNotFoundError:
            print(f"Error: File '{self.file_path}' not found. Creating a new focus table.")
            return self.create_base_focus_table()
        except Exception as e:
            print(f"Error loading focus table: {e}")
            return []

    def save_focus_table(self) -> None:
        """Saves the current focus table to the JSON file."""
        try:
            with open(self.file_path, 'w', encoding='utf-8') as f:
                json.dump([task.__dict__ for task in self.focus_table], f, indent=2)
        except Exception as e:
            print(f"Error saving focus table: {e}")

    def create_base_focus_table(self) -> List[Task]:
        """Creates a base focus table with some example tasks and saves it to the file."""
        base_tasks = [
            Task(name="Analyze code and identify areas for improvement",
                 focus_type="empty",
                 moscow_category="...",
                 importance=0,
                 difficulty=0,
                 reward=0,
                 total_work=0.0,
                 proposed_action=".....",
                 cost_per_run=1.0),
            Task(name="....",
                 focus_type="....",
                 moscow_category="....",
                 importance=0,
                 difficulty=0,
                 reward=0,
                 total_work=0.0,
                 proposed_action=".....",
                 cost_per_run=0.0),
            Task(name="...",
                 focus_type="...",
                 moscow_category="...",
                 importance=0,
                 difficulty=0,
                 reward=0,
                 total_work=0.0,
                 proposed_action="....",
                 cost_per_run=0.0)
        ]

        # Save the base tasks to the file:
        self.focus_table = base_tasks
        self.save_focus_table()
        return base_tasks

    def get_focus_table(self) -> List[Task]:
        """Returns the current focus table."""
        return self.focus_table

    def add_task(self, **kwargs) -> str:
        """Adds a new task to the focus table."""
        new_task = Task(**kwargs)
        self.focus_table.append(new_task)
        self.save_focus_table()
        return f"Task '{new_task.name}' added to the focus table."

    def update_task(self, task_name: str, **kwargs) -> str:
        """Updates a task in the focus table."""
        for task in self.focus_table:
            if task.name == task_name:
                for key, value in kwargs.items():
                    if hasattr(task, key):
                        setattr(task, key, value)
                self.save_focus_table()
                return f"Task '{task_name}' updated in the focus table."
        return f"Task '{task_name}' not found in the focus table."

    def remove_task(self, task_name: str) -> str:
        """Removes a task from the focus table."""
        self.focus_table = [task for task in self.focus_table if task.name != task_name]
        self.save_focus_table()
        return f"Task '{task_name}' removed from the focus table."

    def get_current_focus(self, emotions: Dict[str, int] = None, resources: Dict[str, float] = None) -> Optional[Task]:
        """Determines and returns the task with the highest calculated score, considering emotions and resources."""

        if not self.focus_table:
            return None

        for task in self.focus_table:
            task.calculated_score = self.calculate_score(task, emotions, resources)

        sorted_tasks = sorted(self.focus_table, key=lambda x: x.calculated_score, reverse=True)

        selected_task = sorted_tasks[0]
        self.update_focus_stats(selected_task)
        return selected_task

    def update_focus_stats(self, task: Task):
        task.last_focused = datetime.datetime.now()
        if task.difficulty > 7:
            self.consecutive_difficult_tasks += 1
        else:
            self.consecutive_difficult_tasks = 0
        self.last_focus_type = task.focus_type

    def periodic_review(self):
        # Implement periodic review logic here
        pass

    def manage_dependencies(self):
        for task in self.focus_table:
            task.can_start = all(self.is_task_completed(dep) for dep in task.dependencies)

    def is_task_completed(self, task_name: str) -> bool:
        return any(task.name == task_name and task.status == "COMPLETED" for task in self.focus_table)

    def print_focus_table(self):
        """Prints the focus table in a nicely formatted way using PrettyTable."""

        table = PrettyTable()
        table.field_names = ["Name", "Focus Type", "Moscow", "Importance", "Difficulty", "Reward",
                             "Work Done", "Status", "Dependencies", "Deadline", "Score"]

        for task in self.focus_table:
            deadline_str = task.deadline.strftime("%Y-%m-%d") if task.deadline else ""
            table.add_row([task.name, task.focus_type, task.moscow_category, task.importance,
                           task.difficulty, task.reward, task.work_done, task.status,
                           ", ".join(task.dependencies), deadline_str, f"{task.calculated_score:.2f}"])

        print(table)