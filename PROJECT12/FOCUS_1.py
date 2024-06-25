import time
import numpy as np
from typing import List, Dict, Tuple
from enum import Enum
from collections import deque
from prettytable import PrettyTable


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
    def __init__(self):
        self.focus_tree: Dict[str, FocusPoint] = {}
        self.current_focus: FocusPoint = None
        self.last_update_time = time.time()
        self.exploration_rate = 0.2
        self.noise_level = 0.1
        self.focus_shifts = 0
        self.total_focus_duration = 0.0
        self.focus_history = deque(maxlen=1000)

    def add_focus_point(self, name: str, focus_type: FocusType, moscow_category: MoscowCategory,
                        importance: float, difficulty: float, reward: float, total_work: float,
                        proposed_action: str, cost_per_run: float, parent_name: str = None) -> FocusPoint:
        focus_point = FocusPoint(name, focus_type, moscow_category, importance, difficulty, reward, total_work,
                                 proposed_action, cost_per_run)
        self.focus_tree[name] = focus_point
        if parent_name and parent_name in self.focus_tree:
            self.focus_tree[parent_name].add_child(focus_point)
        return focus_point

    def process_stimulus(self, stimulus_strength: float):
        if stimulus_strength > 0.7 and self.current_focus.focus_type != FocusType.REACTIVE:
            reactive_points = [fp for fp in self.focus_tree.values() if fp.focus_type == FocusType.REACTIVE]
            if reactive_points:
                self.current_focus = max(reactive_points, key=lambda fp: fp.importance * stimulus_strength)
                self.record_focus_shift(self.current_focus.name, "Reactive")
                print(f"Reactive focus shift to: {self.current_focus.name}")

    def select_focus(self):
        if np.random.random() < self.exploration_rate:
            self.current_focus = np.random.choice(list(self.focus_tree.values()))
            self.record_focus_shift(self.current_focus.name, "Exploration")
            print(f"Exploring new focus: {self.current_focus.name}")
        else:
            scores = {name: fp.calculate_score(self.noise_level) for name, fp in self.focus_tree.items()}
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

    def run_simulation(self, duration: float):
        end_time = time.time() + duration
        self.select_focus()


        while time.time() < end_time:
            delta_time = time.time() - self.last_update_time
            self.update_focus(delta_time)

            if np.random.random() < 0.1:
                self.process_stimulus(np.random.random())

            self.print_status()

            self.last_update_time = time.time()
            time.sleep(1)

        self.print_evaluation()

    def print_status(self):
        table = PrettyTable()
        table.field_names = ["Name", "Focus Strength", "Completion (%)", "Predicted Reward", "Predicted Cost", "Turns"]

        for name, fp in self.focus_tree.items():
            table.add_row([
                name,
                f"{fp.focus_strength:.2f}",
                f"{fp.completion_percentage():.1f}%",
                f"{fp.predicted_future_reward:.2f}",
                f"{fp.predicted_future_cost:.2f}",
                fp.turns_taken
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


# Example usage
manager = FocusManager()

manager.add_focus_point("Survive Winter", FocusType.GOAL_ORIENTED, MoscowCategory.MUST, 1.0, 0.9, 1.0, 1000,
                        "Prepare supplies", 50)
manager.add_focus_point("Find Food", FocusType.GOAL_ORIENTED, MoscowCategory.SHOULD, 0.8, 0.6, 0.9, 100,
                        "Scout for food sources", 30, "Survive Winter")
manager.add_focus_point("Hunt Prey", FocusType.GOAL_ORIENTED, MoscowCategory.COULD, 0.7, 0.7, 0.8, 50, "Set traps", 20,
                        "Find Food")
manager.add_focus_point("Forage Berries", FocusType.GOAL_ORIENTED, MoscowCategory.COULD, 0.5, 0.3, 0.4, 30,
                        "Identify safe berries", 10, "Find Food")
manager.add_focus_point("Build Shelter", FocusType.GOAL_ORIENTED, MoscowCategory.SHOULD, 0.6, 0.8, 0.7, 200,
                        "Gather materials", 40, "Survive Winter")
manager.add_focus_point("React to Danger", FocusType.REACTIVE, MoscowCategory.MUST, 0.9, 0.2, 1.0, 10, "Assess threats",
                        5)
manager.add_focus_point("Self-Reflection", FocusType.INTERNAL, MoscowCategory.COULD, 0.4, 0.5, 0.6, 50, "Meditate", 15)

manager.run_simulation(duration=120)


"""

This Python code implements a simulated Focus Manager using a hierarchical system of Focus Points. Here's a breakdown of its key components and functionality:
1. Focus Points:
Represent tasks or goals: Each FocusPoint holds information about a specific task or objective.
Attributes:
name: Identifier of the focus point.
focus_type: (REACTIVE, GOAL_ORIENTED, INTERNAL) - How the task is triggered.
moscow_category: (MUST, SHOULD, COULD, WONT) - Prioritization level.
importance, difficulty, reward, total_work: Parameters influencing task value.
proposed_action, cost_per_run: Description of the action and its associated cost.
parent: Allows for creating a tree-like structure of related focus points.
Various other attributes track progress, focus level, frustration, and historical data.
2. Focus Manager:
Orchestrates focus allocation: The FocusManager class manages the overall focus allocation process.
Key methods:
add_focus_point(): Adds a new focus point to the system.
process_stimulus(): Simulates external events that might trigger reactive focus shifts.
select_focus(): Chooses the next focus point based on exploration or calculated scores.
update_focus(): Updates the state of all focus points over time (focus decay, work done, cost accumulation).
run_simulation(): Runs the simulation for a specified duration.
print_status(), print_evaluation(): Provide insights into the simulation's progress and outcome.
3. Simulation Logic:
Time-based updates: The simulation progresses in discrete time steps.
Focus dynamics:
The currently focused task gains focus strength, allowing work to be done.
Other tasks experience focus decay.
Frustration can build up if a task is focused on for too long.
Excessive cost can also lead to focus shifts.
Stimulus processing: Random external events can interrupt the current focus if a reactive task is more important.
Focus selection:
A balance between exploration (trying new tasks) and exploitation (focusing on high-scoring tasks) is maintained.
Scores consider factors like importance, predicted reward, difficulty, and cost.
Example Usage:

"""