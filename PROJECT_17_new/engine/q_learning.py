import numpy as np

class EnhancedQLearning:
    def __init__(self, states, actions, alpha=0.1, gamma=0.95, epsilon=1.0, 
                 epsilon_decay=0.995, epsilon_min=0.01):
        """Initializes the Q-learning agent.

        Args:
            states (int): The number of possible states.
            actions (int): The number of possible actions.
            alpha (float): The learning rate (0 < alpha <= 1).
            gamma (float): The discount factor (0 <= gamma <= 1).
            epsilon (float): The exploration rate (0 <= epsilon <= 1).
            epsilon_decay (float): The rate at which epsilon decays.
            epsilon_min (float): The minimum value of epsilon.
        """

        self.states = states
        self.actions = actions
        self.alpha = alpha
        self.gamma = gamma
        self.epsilon = epsilon
        self.epsilon_decay = epsilon_decay
        self.epsilon_min = epsilon_min

        # Initialize Q-table with zeros (or small random values)
        self.q_table = np.zeros((states, actions))

    def get_best_action(self, state):
        """Chooses the best action for the given state.

        Args:
            state (int): The current state.

        Returns:
            int: The index of the best action.
        """
        # Exploit: Choose the action with the highest Q-value.
        if np.random.rand() > self.epsilon:
            action = np.argmax(self.q_table[state, :])
        # Explore: Choose a random action.
        else:
            action = np.random.randint(0, self.actions)
        return action

    def update(self, state, action, reward, next_state):
        """Updates the Q-table based on the experience.

        Args:
            state (int): The current state.
            action (int): The action taken.
            reward (float): The reward received.
            next_state (int): The next state.
        """
        # Q-learning update rule:
        self.q_table[state, action] = (1 - self.alpha) * self.q_table[state, action] + \
                                     self.alpha * (reward + self.gamma * np.max(self.q_table[next_state, :]))

        # Decay epsilon
        if self.epsilon > self.epsilon_min:
            self.epsilon *= self.epsilon_decay

    # Enhancements:
    # You can add methods here for:
    # - Saving and loading the Q-table.
    # - Implementing eligibility traces for faster learning.
    # - Using a neural network as a function approximator (Deep Q-learning).
    # - Prioritizing experience replay.
    # - ... and other enhancements to improve performance!