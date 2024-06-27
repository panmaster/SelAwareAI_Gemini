# FOCUS.py
import time
import numpy as np
from typing import List, Dict, Tuple
from enum import Enum
from collections import deque
from prettytable import PrettyTable
import json
class FocusType(Enum):
    REACTIVE = 1
    GOAL_ORIENTED = 2
    INTERNAL = 3

class MoscowCategory(Enum):
    MUST = 4
    SHOULD = 3
    COULD = 2
    WONT = 1

class FocusPoint:
    def __init__(self, name: str, focus_type: FocusType, moscow_category: MoscowCategory,
                 importance: float, difficulty: float, reward: float, total_work: float,
                 proposed_action: str, cost_per_run: float, parent: 'FocusPoint' = None):
        self.name = name
        self.focus_type = focus_type
        self.moscow_category = moscow_category
        self.importance = importance
        self.difficulty = difficulty
        self.reward = reward
        self.total_work = total_work
        self.work_done = 0.0
        self.focus_strength = 0.0
        self.frustration = 0.0
        self.last_focus_time = time.time()
        self.parent = parent
        self.children: List[FocusPoint] = []
        self.accumulated_cost = 0.0
        self.frustration_threshold = 0.8
        self.focus_history = deque(maxlen=100)
        self.cost_history = deque(maxlen=100)
        self.predicted_future_reward = reward
        self.predicted_future_cost = total_work
        self.proposed_action = proposed_action
        self.cost_per_run = cost_per_run
        self.turns_taken = 0
        self.growth_rate = 0.1
        self.decline_rate = 0.05

    def add_child(self, child: 'FocusPoint'):
        self.children.append(child)
        child.parent = self

    def update_focus(self, delta_time: float, is_current_focus: bool):
        current_time = time.time()
        time_passed = current_time - self.last_focus_time

        if is_current_focus:
            growth = self.growth_rate * np.log1p(time_passed) * delta_time
            self.focus_strength = min(1.0, self.focus_strength + growth)
            work_done = self.difficulty * self.focus_strength * delta_time
            self.work_done = min(self.total_work, self.work_done + work_done)
            cost = delta_time * self.difficulty * self.cost_per_run
            self.accumulated_cost += cost
            self.focus_history.append((current_time, self.focus_strength))
            self.cost_history.append((current_time, cost))
            self.turns_taken += 1
        else:
            decay = self.decline_rate * np.exp(-time_passed / 3600) * delta_time
            self.focus_strength = max(0.0, self.focus_strength - decay)

        self.last_focus_time = current_time
        self.update_predictions()

    def update_predictions(self):
        progress = self.work_done / self.total_work
        self.predicted_future_reward = self.reward * (1 - progress)
        self.predicted_future_cost = (self.total_work - self.work_done) * (
            self.accumulated_cost / self.work_done if self.work_done > 0 else 1)

    def calculate_score(self, noise_level: float = 0.0) -> float:
        progress = self.work_done / self.total_work
        base_score = (self.importance * self.predicted_future_reward * self.moscow_category.value) / (
                self.difficulty * (1 + self.frustration) * self.predicted_future_cost)
        noise = np.random.normal(0, noise_level)
        return base_score + noise

    def completion_percentage(self) -> float:
        return (self.work_done / self.total_work) * 100

class FocusManager:
    def __init__(self, human_like=False):
        self.focus_tree: Dict[str, FocusPoint] = {}
        self.current_focus: FocusPoint = None
        self.last_update_time = time.time()
        self.exploration_rate = 0.2 if human_like else 0.05
        self.noise_level = 0.1
        self.focus_shifts = 0
        self.total_focus_duration = 0.0
        self.focus_history = deque(maxlen=1000)
        self.human_like = human_like

    def remove_focus_point(self, name: str) -> bool:
        """Removes a focus point from the focus tree."""
        if name in self.focus_tree:
            focus_point = self.focus_tree[name]
            if focus_point.parent:
                focus_point.parent.children.remove(focus_point)
            for child in focus_point.children:
                child.parent = None
            del self.focus_tree[name]
            if self.current_focus and self.current_focus.name == name:
                self.select_focus()
            return True
        return False

    def add_focus_point(self, name: str, focus_type: FocusType, moscow_category: MoscowCategory,
                        importance: float, difficulty: float, reward: float, total_work: float,
                        proposed_action: str, cost_per_run: float, parent_name: str = None) -> FocusPoint:
        focus_point = FocusPoint(name, focus_type, moscow_category, importance, difficulty, reward, total_work,
                                 proposed_action, cost_per_run)
        self.focus_tree[name] = focus_point
        if parent_name and parent_name in self.focus_tree:
            self.focus_tree[parent_name].add_child(focus_point)
        return focus_point

    def process_stimulus(self, stimulus_strength: float, selection_strategy: str = "highest_importance"):
        if stimulus_strength > 0.7 and self.current_focus.focus_type != FocusType.REACTIVE:
            reactive_points = [fp for fp in self.focus_tree.values() if fp.focus_type == FocusType.REACTIVE]
            if reactive_points:
                if selection_strategy == "highest_importance":
                    self.current_focus = max(reactive_points, key=lambda fp: fp.importance * stimulus_strength)
                elif selection_strategy == "random":
                    self.current_focus = np.random.choice(reactive_points)
                else:
                    raise ValueError(f"Unknown selection strategy: {selection_strategy}")
                self.record_focus_shift(self.current_focus.name, f"Reactive ({selection_strategy})")
                print(f"Reactive focus shift to: {self.current_focus.name}")

    def add_focus_point_from_ai(self, focus_info: Dict) -> str:
        """Adds a focus point suggested by the AI."""
        focus_name = focus_info.get("focus_name")
        focus_type = FocusType[focus_info.get("focus_type", "GOAL_ORIENTED").upper()]
        moscow_category = MoscowCategory[focus_info.get("moscow_category", "SHOULD").upper()]
        importance = float(focus_info.get("importance", 0.5))
        difficulty = float(focus_info.get("difficulty", 0.5))
        reward = float(focus_info.get("reward", 1.0))
        total_work = float(focus_info.get("total_work", 100))
        proposed_action = focus_info.get("proposed_action", "Action not specified")
        cost_per_run = float(focus_info.get("cost_per_run", 10))

        self.add_focus_point(focus_name, focus_type, moscow_category,
                             importance, difficulty, reward, total_work,
                             proposed_action, cost_per_run)
        return f"Focus point '{focus_name}' added successfully."

    def select_focus(self):
        if self.human_like:
            self._select_human_like_focus()
        else:
            self._select_ai_like_focus()

    def _select_human_like_focus(self):
        if np.random.random() < self.exploration_rate:
            self.current_focus = np.random.choice(list(self.focus_tree.values()))
            self.record_focus_shift(self.current_focus.name, "Exploration")
            print(f"Exploring new focus: {self.current_focus.name}")
        else:
            scores = {name: fp.calculate_score(self.noise_level) for name, fp in self.focus_tree.items()}
            self.current_focus = self.focus_tree[max(scores, key=scores.get)]
            self.record_focus_shift(self.current_focus.name, "Score-based")

        self.focus_shifts += 1

    def _select_ai_like_focus(self):
        scores = {name: fp.calculate_score() for name, fp in self.focus_tree.items()}
        self.current_focus = self.focus_tree[max(scores, key=scores.get)]
        self.record_focus_shift(self.current_focus.name, "Score-based")
        self.focus_shifts += 1

    def record_focus_shift(self, focus_name: str, reason: str):
        self.focus_history.append((time.time(), focus_name, reason))

    def update_focus(self, delta_time: float):
        for focus_point in self.focus_tree.values():
            focus_point.update_focus(delta_time, focus_point == self.current_focus)

            if focus_point == self.current_focus:
                self.total_focus_duration += delta_time
                focus_point.frustration += 0.01 * delta_time

                if focus_point.frustration > focus_point.frustration_threshold:
                    print(f"Defocusing from {focus_point.name} due to high frustration")
                    self.select_focus()

                if focus_point.accumulated_cost > focus_point.predicted_future_cost * 1.5:
                    print(f"Defocusing from {focus_point.name} due to high cost")
                    self.select_focus()

    def run_simulation(self, duration: float, sleep_time: float = 1.0):
        end_time = time.time() + duration
        self.select_focus()

        while time.time() < end_time:
            delta_time = time.time() - self.last_update_time
            self.update_focus(delta_time)

            if np.random.random() < 0.1:
                self.process_stimulus(np.random.random())

            self.print_status()

            self.last_update_time = time.time()
            time.sleep(sleep_time)

        self.print_evaluation()

    def print_status(self):
        table = PrettyTable()
        table.field_names = ["Name", "Focus Strength", "Completion (%)", "Predicted Reward", "Predicted Cost",
                             "Accumulated Cost", "Frustration Level", "Turns", "Current Work Done", "Focus Type", "Importance"]

        for name, fp in self.focus_tree.items():
            table.add_row([
                name,
                f"{fp.focus_strength:.2f}",
                f"{fp.completion_percentage():.1f}%",
                f"{fp.predicted_future_reward:.2f}",
                f"{fp.predicted_future_cost:.2f}",
                f"{fp.accumulated_cost:.2f}",
                f"{fp.frustration:.2f}",
                fp.turns_taken,
                f"{fp.work_done:.2f}",
                fp.focus_type.name,
                f"{fp.importance:.2f}"
            ])

        print(f"\nCurrent focus: {self.current_focus.name}")
        print(table)
        print("---")

    def print_evaluation(self):
        print("\nEvaluation Metrics:")
        print(f"Total Focus Shifts: {self.focus_shifts}")
        print(f"Average Focus Duration: {self.total_focus_duration / self.focus_shifts:.2f} seconds")
        print(
            f"Task Completion Rate: {sum(fp.completion_percentage() for fp in self.focus_tree.values()) / len(self.focus_tree):.2f}%")
        print(f"Resource Utilization: {sum(fp.accumulated_cost for fp in self.focus_tree.values()):.2f} total cost")

        print("\nFocus History (last 10 shifts):")
        for timestamp, focus_name, reason in list(self.focus_history)[-10:]:
            print(f"  {time.ctime(timestamp)}: Shifted to {focus_name} ({reason})")

    # New functions to create, add, and update focus points
    def create_focus_topic(self, name: str, focus_type: FocusType, moscow_category: MoscowCategory,
                           importance: float, difficulty: float, reward: float, total_work: float,
                           proposed_action: str, cost_per_run: float) -> FocusPoint:
        """
        Creates a new focus topic (root focus point) in the focus tree.
        """
        return self.add_focus_point(name, focus_type, moscow_category, importance, difficulty, reward,
                                    total_work, proposed_action, cost_per_run)

    def add_focus_point_to_task(self, task_name: str, name: str, focus_type: FocusType, moscow_category: MoscowCategory,
                                importance: float, difficulty: float, reward: float, total_work: float,
                                proposed_action: str, cost_per_run: float) -> FocusPoint:
        """
        Adds a new focus point to an existing task (parent focus point).
        """
        if task_name in self.focus_tree:
            return self.add_focus_point(name, focus_type, moscow_category, importance, difficulty, reward,
                                        total_work, proposed_action, cost_per_run, parent_name=task_name)
        else:
            print(f"Error: Task '{task_name}' not found in the focus tree.")
            return None

    def update_difficulty(self, focus_name: str, new_difficulty: float):
        """
        Updates the difficulty of an existing focus point.
        """
        if focus_name in self.focus_tree:
            self.focus_tree[focus_name].difficulty = new_difficulty
            print(f"Difficulty of focus point '{focus_name}' updated to {new_difficulty}.")
        else:
            print(f"Error: Focus point '{focus_name}' not found in the focus tree.")

    def update_reward(self, focus_name: str, new_reward: float):
        """
        Updates the reward of an existing focus point.
        """
        if focus_name in self.focus_tree:
            self.focus_tree[focus_name].reward = new_reward
            print(f"Reward of focus point '{focus_name}' updated to {new_reward}.")
        else:
            print(f"Error: Focus point '{focus_name}' not found in the focus tree.")

    def update_cost_per_run(self, focus_name: str, new_cost_per_run: float):
        """
        Updates the cost per run of an existing focus point.
        """
        if focus_name in self.focus_tree:
            self.focus_tree[focus_name].cost_per_run = new_cost_per_run
            print(f"Cost per run of focus point '{focus_name}' updated to {new_cost_per_run}.")
        else:
            print(f"Error: Focus point '{focus_name}' not found in the focus tree.")

    def save_state(self, filename: str):
        """Saves the current focus tree state to a file."""
        state = {
            "focus_tree": {name: {
                "name": fp.name,
                "focus_type": fp.focus_type.name,
                "moscow_category": fp.moscow_category.name,
                "importance": fp.importance,
                "difficulty": fp.difficulty,
                "reward": fp.reward,
                "total_work": fp.total_work,
                "work_done": fp.work_done,
                "proposed_action": fp.proposed_action,
                "cost_per_run": fp.cost_per_run,
                "parent": fp.parent.name if fp.parent else None,
                "children": [child.name for child in fp.children]
            } for name, fp in self.focus_tree.items()},
            "current_focus": self.current_focus.name if self.current_focus else None
        }
        with open(filename, 'w') as f:
            json.dump(state, f, indent=2)

    def load_state(self, filename: str):
        """Loads the focus tree state from a file."""
        with open(filename, 'r') as f:
            state = json.load(f)

        self.focus_tree.clear()
        for name, data in state["focus_tree"].items():
            fp = FocusPoint(
                name=data["name"],
                focus_type=FocusType[data["focus_type"]],
                moscow_category=MoscowCategory[data["moscow_category"]],
                importance=data["importance"],
                difficulty=data["difficulty"],
                reward=data["reward"],
                total_work=data["total_work"],
                proposed_action=data["proposed_action"],
                cost_per_run=data["cost_per_run"]
            )
            fp.work_done = data["work_done"]
            self.focus_tree[name] = fp

        for name, data in state["focus_tree"].items():
            if data["parent"]:
                self.focus_tree[name].parent = self.focus_tree[data["parent"]]
            for child_name in data["children"]:
                self.focus_tree[name].children.append(self.focus_tree[child_name])

        if state["current_focus"]:
            self.current_focus = self.focus_tree[state["current_focus"]]
        else:
            self.current_focus = None

    def generate_summary(self) -> str:
            """Generates a summary of the current focus."""
            if self.current_focus:
                return f"{self.current_focus.name} (Importance: {self.current_focus.importance:.2f}, Difficulty: {self.current_focus.difficulty:.2f}, Progress: {self.current_focus.completion_percentage():.1f}%)"
            else:
                return "No current focus."