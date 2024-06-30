import time
import numpy as np
import math
from typing import List, Dict
from enum import Enum
from collections import deque
from prettytable import PrettyTable
import json
import os

FILEPATH = "../PROJECT13/Brain_settings/Focus.json"

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
        self.fatigue = 0.0
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
        self.base_growth_rate = 0.05
        self.base_decline_rate = 0.03
        self.last_update_time = time.time()
        self.attention_span = np.random.uniform(10, 30)  # Random attention span between 10-30 minutes
        self.focus_duration = 0
        self.last_break_time = time.time()
        self.progress_rate = 0.0
        self.resilience = np.random.uniform(0.5, 1.0)  # Resilience against frustration
        self.completed = False
        self.completed_tag = "NOT_COMPLETED"  # Add a tag to indicate completion

    def update_focus(self, current_time: float, is_current_focus: bool):
        time_passed = current_time - self.last_update_time

        if self.completed:
            self.focus_strength = max(0.0, self.focus_strength - (self.base_decline_rate * time_passed))
            return

        if is_current_focus:
            self.focus_duration += time_passed
            attention_factor = self.calculate_attention_factor()
            growth = self.base_growth_rate * math.log1p(time_passed) * attention_factor
            self.focus_strength = min(1.0, self.focus_strength + growth)

            work_done = self.difficulty * self.focus_strength * time_passed * (1 - self.fatigue)
            self.work_done = min(self.total_work, self.work_done + work_done)

            cost = time_passed * self.difficulty * self.cost_per_run
            self.accumulated_cost += cost

            self.focus_history.append((current_time, self.focus_strength))
            self.cost_history.append((current_time, cost))
            self.turns_taken += 1

            self.update_frustration(time_passed)
            self.update_fatigue(time_passed)
            self.update_progress_rate(work_done, time_passed)

            if self.work_done == self.total_work:
                self.completed = True
                self.completed_tag = "COMPLETED"
                self.focus_strength = self.focus_strength / 2  # Halve the focus strength
        else:
            self.focus_duration = 0
            decline_rate = self.base_decline_rate * (1 + self.difficulty)
            decline = decline_rate * time_passed
            self.focus_strength = max(0.0, self.focus_strength - decline)

            self.recover_from_fatigue(time_passed)
            self.reduce_frustration(time_passed)

        self.last_update_time = current_time
        self.update_predictions()

    def calculate_attention_factor(self):
        return max(0, 1 - (self.focus_duration / (self.attention_span * 60)))

    def update_frustration(self, time_passed):
        frustration_increase = time_passed / (self.attention_span * 60)  # Frustration increases as fast as fatigue
        self.frustration = min(1.0, self.frustration + frustration_increase)

    def update_fatigue(self, time_passed):
        fatigue_increase = time_passed / (8 * 60 * 60)  # Assuming 8-hour work day
        self.fatigue = min(1.0, self.fatigue + fatigue_increase)

    def recover_from_fatigue(self, time_passed):
        recovery_rate = 0.5 * time_passed / (60 * 60)  # Recover twice as fast as fatigue builds up
        self.fatigue = max(0.0, self.fatigue - recovery_rate)

    def reduce_frustration(self, time_passed):
        frustration_decrease = 0.01 * time_passed * self.resilience
        self.frustration = max(0.0, self.frustration - frustration_decrease)

    def update_progress_rate(self, work_done, time_passed):
        self.progress_rate = work_done / time_passed if time_passed > 0 else 0

    def update_predictions(self):
        progress = self.work_done / self.total_work
        self.predicted_future_reward = self.reward * (1 - progress)
        self.predicted_future_cost = (self.total_work - self.work_done) * (
            self.accumulated_cost / self.work_done if self.work_done > 0 else 1)

    def calculate_score(self, noise_level: float = 0.0) -> float:
        if self.completed:
            return 0.0  # No score for completed tasks

        progress = self.work_done / self.total_work
        base_score = (self.importance * self.predicted_future_reward * self.moscow_category.value) / (
                self.difficulty * (1 + self.frustration) * self.predicted_future_cost)
        momentum_factor = 1 + (0.1 * self.progress_rate)  # Add momentum to score
        noise = np.random.normal(0, noise_level)
        return base_score * momentum_factor + noise

    def completion_percentage(self) -> float:
        return (self.work_done / self.total_work) * 100

    def take_break(self):
        self.fatigue = max(0, self.fatigue - 0.3)
        self.frustration = max(0, self.frustration - 0.2 * self.resilience)

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
        self.distractibility = np.random.uniform(0.1, 0.3)
        self.last_break_time = time.time()
        self.overall_productivity = 0.0
        self.current_mood = "Neutral"
        self.mood_impact = 0.1  # How much mood affects distractibility
        self.completed_tasks: List[FocusPoint] = []

    def add_focus_point(self, name: str, focus_type: FocusType, moscow_category: MoscowCategory,
                        importance: float, difficulty: float, reward: float, total_work: float,
                        proposed_action: str, cost_per_run: float, parent_name: str = None) -> FocusPoint:
        focus_point = FocusPoint(name, focus_type, moscow_category, importance, difficulty, reward, total_work,
                                 proposed_action, cost_per_run)
        self.focus_tree[name] = focus_point
        if parent_name and parent_name in self.focus_tree:
            parent = self.focus_tree[parent_name]
            parent.children.append(focus_point)
            focus_point.parent = parent
        return focus_point

    def process_stimulus(self, stimulus_strength: float):
        mood_factor = 1.0
        if self.current_mood == "Happy":
            mood_factor = 0.8
        elif self.current_mood == "Sad":
            mood_factor = 1.2
        adjusted_distractibility = self.distractibility * mood_factor

        if self.current_focus and stimulus_strength > adjusted_distractibility and self.current_focus.focus_type != FocusType.REACTIVE:
            reactive_points = [fp for fp in self.focus_tree.values() if fp.focus_type == FocusType.REACTIVE]
            if reactive_points:
                self.current_focus = max(reactive_points, key=lambda fp: fp.importance * stimulus_strength)
                self.record_focus_shift(self.current_focus.name, f"Reactive (Stimulus: {stimulus_strength:.2f})")
                print(f"Reactive focus shift to: {self.current_focus.name}")

    def select_focus(self):
        if not self.current_focus or np.random.random() < self.exploration_rate or self.current_focus.frustration > self.current_focus.frustration_threshold:
            # Prioritize unfinished tasks over completed ones
            available_focus_points = [fp for fp in self.focus_tree.values() if not fp.completed]
            if available_focus_points:
                self.current_focus = np.random.choice(available_focus_points)
            else:
                self.current_focus = np.random.choice(list(self.focus_tree.values()))
            self.record_focus_shift(self.current_focus.name, "Exploration/Frustration")
            print(f"Switching focus to: {self.current_focus.name}")
        else:
            scores = {name: fp.calculate_score(self.noise_level) for name, fp in self.focus_tree.items()}
            self.current_focus = self.focus_tree[max(scores, key=scores.get)]
            self.record_focus_shift(self.current_focus.name, "Highest Score")

    def record_focus_shift(self, focus_name: str, reason: str):
        self.focus_shifts += 1
        self.focus_history.append((time.time(), focus_name, reason))

    def update_focus(self, current_time: float):
        for focus_point in self.focus_tree.values():
            focus_point.update_focus(current_time, is_current_focus=(focus_point is self.current_focus))
        self.total_focus_duration += current_time - self.last_update_time
        self.last_update_time = current_time

        # Move completed tasks to the completed list
        completed_tasks = [fp for fp in self.focus_tree.values() if fp.completed and fp not in self.completed_tasks]
        self.completed_tasks.extend(completed_tasks)

    def FOCUS_NOW(self, time_step=1, stimulus_frequency=0.2):
        current_time = time.time()
        self.update_focus(current_time)

        if np.random.random() < stimulus_frequency:
            stimulus_strength = np.random.random()
            self.process_stimulus(stimulus_strength)

        if self.should_take_break():
            self.take_break()
        elif not self.current_focus or self.current_focus.frustration > self.current_focus.frustration_threshold or np.random.random() < self.exploration_rate:
            self.select_focus()

        self.update_overall_productivity()
        self.summarize()

    def should_take_break(self):
        time_since_last_break = time.time() - self.last_break_time
        return (time_since_last_break > 45 * 60 or  # Take a break every 45 minutes
                (self.current_focus and self.current_focus.fatigue > 0.7) or  # Take a break if too fatigued
                (self.current_focus and self.current_focus.frustration > 0.8))  # Take a break if too frustrated

    def take_break(self):
        print("Taking a break...")
        self.last_break_time = time.time()
        if self.current_focus:
            self.current_focus.take_break()
        time.sleep(5)  # Simulate a 5-second break

    def update_overall_productivity(self):
        total_work_done = sum(fp.work_done for fp in self.focus_tree.values())
        total_work = sum(fp.total_work for fp in self.focus_tree.values())
        self.overall_productivity = total_work_done / total_work if total_work > 0 else 0

    def summarize(self):
        table = PrettyTable()
        table.field_names = ["Focus Point", "Focus Strength", "Type", "Importance", "Difficulty",
                             "Reward", "Total Work", "Completion %", "Frustration", "Fatigue", "Status"]

        for fp in self.focus_tree.values():
            table.add_row([fp.name, f"{fp.focus_strength:.2f}", fp.focus_type.name, fp.importance, fp.difficulty,
                           fp.reward, fp.total_work, f"{fp.completion_percentage():.2f}",
                           f"{fp.frustration:.2f}", f"{fp.fatigue:.2f}", fp.completed_tag])
        print(table)

        completed_table = PrettyTable()
        completed_table.field_names = ["Completed Task", "Completion %", "Status"]
        for task in self.completed_tasks:
            completed_table.add_row([task.name, f"{task.completion_percentage():.2f}", task.completed_tag])
        print("Completed Tasks:")
        print(completed_table)

        print(f"Overall Productivity: {self.overall_productivity:.2%}")
        print(f"Current Mood: {self.current_mood}")

    def save_state(self):
        state = {
            "focus_tree": {name: self.serialize_focus_point(fp) for name, fp in self.focus_tree.items()},
            "current_focus": self.current_focus.name if self.current_focus else None,
            "last_update_time": self.last_update_time,
            "exploration_rate": self.exploration_rate,
            "noise_level": self.noise_level,
            "focus_shifts": self.focus_shifts,
            "total_focus_duration": self.total_focus_duration,
            "distractibility": self.distractibility,
            "last_break_time": self.last_break_time,
            "overall_productivity": self.overall_productivity,
            "current_mood": self.current_mood,
            "completed_tasks": [self.serialize_focus_point(task) for task in self.completed_tasks]
        }
        with open(FILEPATH, 'w') as f:
            json.dump(state, f)

    def load_state(self):
        try:
            with open(FILEPATH, 'r') as f:
                # Check if the file is empty
                if os.stat(FILEPATH).st_size == 0:
                    print("Focus.json is empty. Loading default focus points.")
                    self.add_focus_point(name="What am I experiencing?", focus_type=FocusType.INTERNAL,
                                         moscow_category=MoscowCategory.MUST, importance=0.9, difficulty=0.3,
                                         reward=7, total_work=60, proposed_action="Journal for 15 minutes",
                                         cost_per_run=0.005)

                    self.add_focus_point(name="What am I feeling?", focus_type=FocusType.INTERNAL,
                                         moscow_category=MoscowCategory.SHOULD, importance=0.8, difficulty=0.2,
                                         reward=5, total_work=45,
                                         proposed_action="Reflect on emotions for 10 minutes",
                                         cost_per_run=0.003)

                    self.add_focus_point(name="What's happening around me?", focus_type=FocusType.INTERNAL,
                                         moscow_category=MoscowCategory.COULD, importance=0.7, difficulty=0.4,
                                         reward=4, total_work=30,
                                         proposed_action="Observe my surroundings for 5 minutes",
                                         cost_per_run=0.002)
                else:
                    print("Loading focus points from Focus.json")
                    state = json.load(f)
                    self.focus_tree = {name: self.deserialize_focus_point(fp_data) for name, fp_data in
                                       state["focus_tree"].items()}
                    self.current_focus = self.focus_tree[state["current_focus"]] if state["current_focus"] else None
                    self.last_update_time = state["last_update_time"]
                    self.exploration_rate = state["exploration_rate"]
                    self.noise_level = state["noise_level"]
                    self.focus_shifts = state["focus_shifts"]
                    self.total_focus_duration = state["total_focus_duration"]
                    self.distractibility = state["distractibility"]
                    self.last_break_time = state["last_break_time"]
                    self.overall_productivity = state["overall_productivity"]
                    self.current_mood = state["current_mood"]
                    self.completed_tasks = [self.deserialize_focus_point(task) for task in state["completed_tasks"]]
        except FileNotFoundError:
            print("No saved state found. Starting with a new focus manager. Loading defoult")
            self.add_focus_point(name="What am I experiencing?", focus_type=FocusType.INTERNAL,
                                 moscow_category=MoscowCategory.MUST, importance=0.9, difficulty=0.3,
                                 reward=7, total_work=60, proposed_action="Journal for 15 minutes",
                                 cost_per_run=0.005)

            self.add_focus_point(name="What am I feeling?", focus_type=FocusType.INTERNAL,
                                 moscow_category=MoscowCategory.SHOULD, importance=0.8, difficulty=0.2,
                                 reward=5, total_work=45, proposed_action="Reflect on emotions for 10 minutes",
                                 cost_per_run=0.003)

            self.add_focus_point(name="What's happening around me?", focus_type=FocusType.INTERNAL,
                                 moscow_category=MoscowCategory.COULD, importance=0.7, difficulty=0.4,
                                 reward=4, total_work=30, proposed_action="Observe my surroundings for 5 minutes",
                                 cost_per_run=0.002)

    def serialize_focus_point(self, fp: FocusPoint) -> dict:
        return {
            "name": fp.name,
            "focus_type": fp.focus_type.value,
            "moscow_category": fp.moscow_category.value,
            "importance": fp.importance,
            "difficulty": fp.difficulty,
            "reward": fp.reward,
            "total_work": fp.total_work,
            "work_done": fp.work_done,
            "focus_strength": fp.focus_strength,
            "frustration": fp.frustration,
            "fatigue": fp.fatigue,
            "accumulated_cost": fp.accumulated_cost,
            "proposed_action": fp.proposed_action,
            "cost_per_run": fp.cost_per_run,
            "parent": fp.parent.name if fp.parent else None,
            "children": [child.name for child in fp.children],
            "resilience": fp.resilience,
            "completed": fp.completed,
            "completed_tag": fp.completed_tag
        }

    def deserialize_focus_point(self, data: dict) -> FocusPoint:
        fp = FocusPoint(
            name=data["name"],
            focus_type=FocusType(data["focus_type"]),
            moscow_category=MoscowCategory(data["moscow_category"]),
            importance=data["importance"],
            difficulty=data["difficulty"],
            reward=data["reward"],
            total_work=data["total_work"],
            proposed_action=data["proposed_action"],
            cost_per_run=data["cost_per_run"]
        )
        fp.work_done = data["work_done"]
        fp.focus_strength = data["focus_strength"]
        fp.frustration = data["frustration"]
        fp.fatigue = data["fatigue"]
        fp.accumulated_cost = data["accumulated_cost"]
        fp.resilience = data["resilience"]
        fp.completed = data["completed"]
        fp.completed_tag = data["completed_tag"]

        if data["parent"]:
            fp.parent = self.focus_tree[data["parent"]]
        if "children" in data:
            fp.children = [self.focus_tree[child_name] for child_name in data["children"]]

        return fp

if __name__ == "__main__":
    import os

    fm = FocusManager()
    fm.load_state()  # Try to load saved state

    # Example Focus Points
    fm.add_focus_point(name="Write a report", focus_type=FocusType.GOAL_ORIENTED,
                        moscow_category=MoscowCategory.MUST, importance=0.9, difficulty=0.6,
                        reward=10, total_work=120, proposed_action="Open document and start writing",
                        cost_per_run=0.01)
    fm.add_focus_point(name="Clean the kitchen", focus_type=FocusType.GOAL_ORIENTED,
                        moscow_category=MoscowCategory.SHOULD, importance=0.7, difficulty=0.4,
                        reward=6, total_work=60, proposed_action="Put on gloves and start cleaning",
                        cost_per_run=0.005)
    fm.add_focus_point(name="Learn a new skill", focus_type=FocusType.GOAL_ORIENTED,
                        moscow_category=MoscowCategory.COULD, importance=0.6, difficulty=0.8,
                        reward=8, total_work=90, proposed_action="Open online course and start learning",
                        cost_per_run=0.008)

    fm.add_focus_point(name="Respond to email", focus_type=FocusType.REACTIVE,
                        moscow_category=MoscowCategory.MUST, importance=0.8, difficulty=0.2,
                        reward=3, total_work=15, proposed_action="Open email and reply",
                        cost_per_run=0.002)

    # Main loop
    while True:
        fm.FOCUS_NOW(time_step=1, stimulus_frequency=0.2)
        time.sleep(1)  # Simulate 1-second time step
        fm.save_state()  # Save the current state before exiting