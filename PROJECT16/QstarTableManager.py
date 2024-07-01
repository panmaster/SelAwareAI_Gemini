#QstarTableManager.py
import random
from typing import Dict, Tuple, Any
from typing import List
import  json
class State:
    def __init__(self, current_project: str, current_task: str, emotions: Dict[str, float]):
        self.current_project = current_project
        self.current_task = current_task
        self.emotions = emotions



    def __str__(self):
        return f"Project: {self.current_project}, Task: {self.current_task}, Emotions: {self.emotions}"

    def __hash__(self):
        return hash((self.current_project, self.current_task, tuple(self.emotions.items())))

    def __eq__(self, other):
        return isinstance(other, State) and self.__dict__ == other.__dict__

class QstarTable:
    def __init__(self, learning_rate: float = 0.1, discount_factor: float = 0.9, exploration_rate: float = 0.1):
        self.q_table: Dict[State, Dict[str, float]] = {}
        self.learning_rate = learning_rate
        self.discount_factor = discount_factor
        self.exploration_rate = exploration_rate
        self.actions = ["select_project", "start_task", "complete_task", "switch_task"]


    def initialize_table(self, actions: List[str]):
        """Initializes the Q-table with default values for each action."""
        self.actions = actions  # Store the actions
        for state in self.q_table:
            for action in actions:
                self.q_table[state][action] = 0.0



    def get_q_value(self, state: State, action: str) -> float:
        if state not in self.q_table:
            self.q_table[state] = {a: 0.0 for a in self.actions}
        return self.q_table[state].get(action, 0.0)

    def update_q_value(self, state: State, action: str, reward: float, next_state: State) -> None:
        if state not in self.q_table:
            self.q_table[state] = {a: 0.0 for a in self.actions}

        best_future_q = max(self.get_q_value(next_state, a) for a in self.actions)
        current_q = self.q_table[state][action]
        new_q = current_q + self.learning_rate * (reward + self.discount_factor * best_future_q - current_q)
        self.q_table[state][action] = new_q

    def choose_best_action(self, state: State) -> str:
        if random.uniform(0, 1) < self.exploration_rate:
            return random.choice(self.actions)
        else:
            if state not in self.q_table:
                return random.choice(self.actions)
            return max(self.q_table[state], key=self.q_table[state].get)

    def save_q_table(self, filename: str):
        with open(filename, 'w') as f:
            json.dump({str(k): v for k, v in self.q_table.items()}, f)

    def load_q_table(self, filename: str):
        with open(filename, 'r') as f:
            data = json.load(f)
            self.q_table = {eval(k): v for k, v in data.items()}