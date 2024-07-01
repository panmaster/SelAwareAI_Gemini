import random
from typing import Dict, Tuple, Any

class State:
    def __init__(self, **kwargs):
        # Define state attributes here, e.g.:
        self.focus = kwargs.get("focus", "")
        self.emotions = kwargs.get("emotions", {})
        # ... add other state attributes as needed ...

    def __str__(self):
        return str(self.__dict__)

    def __hash__(self):
        # Define a hash function to make states hashable for use in dictionaries
        return hash(str(self))

    def __eq__(self, other):
        # Define equality for states
        return isinstance(other, State) and self.__dict__ == other.__dict__

class QstarTable:
    def __init__(self, learning_rate: float = 0.1, discount_factor: float = 0.9, exploration_rate: float = 0.1):
        self.q_table: Dict[State, Dict[str, float]] = {}
        self.learning_rate = learning_rate
        self.discount_factor = discount_factor
        self.exploration_rate = exploration_rate
        self.actions = []  # You need to define the possible actions for your AI

    table_file = "Brain_settings/ProjectTable/projecttable_table.json"
    def initialize_table(self, actions: List[str]):
        """Initializes the Q-table with random values."""
        self.actions = actions
        for action in self.actions:
            self.q_table[action] = {} 

    def get_q_value(self, state: State, action: str) -> float:
        """Gets the Q-value for a given state-action pair."""
        if state not in self.q_table:
            self.q_table[state] = {a: 0.0 for a in self.actions}
        return self.q_table[state].get(action, 0.0)

    def update_q_value(self, state: State, action: str, reward: float, next_state: State) -> None:
        """Updates the Q-value using the Q-learning algorithm."""
        if state not in self.q_table:
            self.q_table[state] = {a: 0.0 for a in self.actions}

        best_future_q = max(self.get_q_value(next_state, a) for a in self.actions)
        new_q = self.get_q_value(state, action) + self.learning_rate * (
                reward + self.discount_factor * best_future_q - self.get_q_value(state, action)
        )
        self.q_table[state][action] = new_q

    def choose_best_action(self, state: State) -> str:
        """Chooses the best action for the given state."""
        if random.uniform(0, 1) < self.exploration_rate:
            return random.choice(self.actions)  # Exploration
        else:
            q_values = [self.get_q_value(state, action) for action in self.actions]
            best_action_index = q_values.index(max(q_values))
            return self.actions[best_action_index]  # Exploitation