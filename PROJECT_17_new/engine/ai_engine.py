## ai_engine.py
import google.generativeai as genai
from state_manager import StateManager
from q_learning import EnhancedQLearning
from  .. generation.loop_generator import    LoopGenerator
from .. loops.awareness_loop import  Initialise_Awarness_Loop_Models

api_key = "AIzaSyA60tGw6fZwQdamW8sm6pkgRh5W559kLJ0"
def main():

    ai_system = AdvancedAISystem(api_key)




main()













class AdvancedAISystem:
    def __init__(self, api_key, tools_directory="tools"):
        self.api_key = api_key
        genai.configure(api_key=api_key)

        self.loop_manager = LoopManager(self)
        self.state_manager = StateManager()

        # Get loop names after LoopManager initialization
        loop_names = self.loop_manager.get_loop_names()
        self.q_learning = EnhancedQLearning(states=100, actions=loop_names)
        self.loop_generator = LoopGenerator(self)



