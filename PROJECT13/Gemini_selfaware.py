# Gemini_selfaware.py
import os
import datetime
import json
import time

import google.generativeai as genai
from memory_frame_creation import CREATE_MEMORY_FRAME
from Tool_Manager import ToolManager
import traceback

from typing import List

from SelAwareAI_Gemini.TESTOWE.FOCUS import FocusManager, FocusType, MoscowCategory



import ast
import re
from typing import Any, Dict, Optional

# Configuration
genai.configure(api_key='AIzaSyA60tGw6fZwQdamW8sm6pkgRh5W559kLJ0')  # Replace with your actual API key
SESSION_FOLDER, MEMORY_FOLDER = "sessions", "memories"
MEMORY_STRUCTURE_SUMMARY_FILE = "memory_structure_summary.txt"

# ANSI escape codes for text colors


WHITE = '\033[97m'
HEADER = '\033[95m'
OKBLUE = '\033[94m'
OKCYAN = '\033[96m'
OKGREEN = '\033[92m'
WARNING = '\033[93m'
FAIL = '\033[91m'
ENDC = '\033[0m'
BOLD = '\033[1m'
UNDERLINE = '\033[4m'
WHITE = '\033[97m'
YELLOW = '\033[93m'
MAGENTA = '\033[95m'
LIGHTBLUE = '\033[94m'


def safe_json_parse(json_string: str) -> Optional[Dict[str, Any]]:
    try:
        return json.loads(json_string)
    except json.JSONDecodeError as e:
        print(f"Warning: Could not parse JSON: {e}")
        print(f"Raw text: {json_string}")
        return None

class Task:
    def __init__(self, name, focus_type, moscow_category, importance, difficulty, reward, total_work, proposed_action, cost_per_run, work_done=0.0, focus_strength=0.0, frustration=0.0, fatigue=0.0, accumulated_cost=0.0, status="NOT_COMPLETED", learned_knowledge="", important_facts="", current_focus=False, goal="", dependencies=[], deadline=None):
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


class GeminiSelfAwareAI:
    def __init__(self):
        self.session_info = self.create_session_info()
        self.conversation_log_path = os.path.join(self.session_info['session_path'], "conversation_log.txt")
        self.tool_manager = ToolManager()
        self.iteration_count = 0
        self.user_input_count = 0
        self.function_call_results = ""
        self.current_conversation_frame = ""
        self.sensory_inputs = {"text": "None", "visual": "None", "audio": "None", "previous_action_results": None}
        self.action_response_text = ""
        self.state_of_mind = {}
        self.prompts = {}
        self.emotions = {}
        self.long_term_memory = []
        self.context_window = []
        self.valid_tool_types = {"all", "input", "reflection", "action", "web", "emotions"}
        self.initialize()


    def initialize(self):
        self.state_of_mind = self.load_state_of_mind()
        self.prompts = self.load_prompts()
        self.emotions = self.load_emotions()
        self.initialize_models()

    def initialize_models(self):
        response = genai.list_models()
        if not response:
            raise ValueError("Invalid or expired API key")
        """Initializes the Gemini models for different stages."""
        try:
            alltools_str = self.tool_manager.get_tools_list_json("all")
            alltools = ast.literal_eval(alltools_str)

            input_tools_str = self.tool_manager.get_tools_list_json("input")
            input_tools = ast.literal_eval(input_tools_str)



            reflection_tools_str = self.tool_manager.get_tools_list_json("reflection")
            reflection_tools = ast.literal_eval(reflection_tools_str)






            input_instruction = """
                          You are an AI assistant analyzing current inputs and the AI's state.
                          Identify the most critical focus area and provide your response as:
                          FocusOn: [identified focus]
                          Answer questions:
                          1.What do i want?
                          2.what do i need?
                          3.what do i plan to do ?
                          4.what  am i feeling ?
                          5.what am i expiriancing ?
                          """

            reflection_instruction = """
                          You are a reflective AI assistant analyzing the input stage's output (including potential memories).
                          Provide insights, identify patterns, suggest a concise action plan for the action model, and determine the FocusLevel for the next iteration:
                          FocusLevel: [a float between 0 and 1]
                          """

            action_instruction = """
                          You are an action-oriented AI assistant. Execute the action plan provided by the reflection stage using available tools.
                          Justify your chosen actions and their expected impact. 
                          """

            emotion_instruction = """
                          You are an emotion-analysis AI assistant evaluating recent events, actions, and outcomes.
                          Provide a concise JSON object with emotion adjustments (keys: emotion names, values: intensity 0-100). 
                          """

            learning_instruction = """
                          You are a learning-focused AI assistant analyzing the results of the action stage.
                          Identify new knowledge or skills for long-term improvement and summarize recommendations concisely. 
                          """
            try:
                self.input_model = genai.GenerativeModel(
                    system_instruction=input_instruction,
                    model_name="gemini-1.5-flash-latest",
                    tools=alltools)
                self.input_chat = self.input_model.start_chat(history=[])
            except Exception as E:
                print("faild to initialise  input  model")
                print(E)

            try:
                self.reflection_model = genai.GenerativeModel(
                    system_instruction=reflection_instruction,
                    model_name="gemini-1.5-flash-latest",
                    safety_settings={"HARASSMENT": "block_none"},
                    tools=alltools)
                self.reflection_chat = self.reflection_model.start_chat(history=[])
            except Exception as e:
                print(e)

            try:
                self.action_model = genai.GenerativeModel(
                    system_instruction=action_instruction,
                    model_name="gemini-1.5-flash-latest",
                    safety_settings={"HARASSMENT": "block_none"},
                    tools=reflection_tools)
                self.action_chat = self.action_model.start_chat(history=[])
            except Exception as e:
                print("faild  to initialise")
                print(e)

            self.emotion_model = genai.GenerativeModel(
                system_instruction=emotion_instruction,
                model_name="gemini-1.5-flash-latest",
                safety_settings={"HARASSMENT": "block_none"})
            self.emotion_chat = self.emotion_model.start_chat(history=[])

            self.learning_model = genai.GenerativeModel(
                system_instruction=learning_instruction,
                model_name="gemini-1.5-flash-latest",
                safety_settings={"HARASSMENT": "block_none"})
            self.learning_chat = self.learning_model.start_chat(history=[])

            print(f"{OKGREEN}Models initialized successfully!{ ENDC}")
        except Exception as E:
            raise RuntimeError(f"{ FAIL}Error initializing models: {E}{ ENDC}")









    def load_state_of_mind(self):
        """Loads state of mind from Focus.json."""
        try:
            with open("Brain_settings/Focus.json", 'r') as f:
                return json.load(f)
        except FileNotFoundError:

            return {"FocusOn": "", "FocusLevel": 0.0}

    def load_prompts(self):
        """Loads prompts from prompts.json."""
        try:
            with open("Brain_settings/prompts.json", 'r') as f:
                return json.load(f)
        except FileNotFoundError:

            return {
                "input": "Analyze current inputs, state, and emotions. What's the most important aspect to focus on?  You can call the 'retrieve_memories' function to access past relevant memories.  Provide your response in the following format:\n FocusOn: [identified focus]\n FocusLevel: [a float between 0 and 1]",
                "reflection": "Reflect on recent actions, outcomes, and emotional states. What insights can be drawn? Consider potential improvements or adjustments to behavior and decision-making.  You can also call the 'retrieve_memories' function to access relevant memories.  Format your response to be clear and structured, highlighting key observations and recommendations.",
                "action": "Based on the current focus, reflections, and emotional state, what is the optimal next action? If necessary, use available tools to perform actions.  Always justify your chosen action and explain its expected impact. You can also call the 'retrieve_memories' function to access relevant memories.",
                "emotion": "Based on recent events and outcomes, how should my emotional state be adjusted?  Provide your response as a JSON object with emotion names as keys and values between 0 and 100, representing the intensity of each emotion.",
                "learning": "What new knowledge or skills should be prioritized for long-term improvement based on recent experiences and outcomes? Summarize your insights and recommendations in a concise, structured format that can be easily integrated into the learning system."
            }

    def load_emotions(self):
        """Loads emotions from emotions.json."""
        try:
            with open("Brain_settings/emotions.json", 'r') as f:
                return json.load(f)
        except FileNotFoundError:

            return {
                "happiness": 50,
                "sadness": 50,
                "anger": 50,
                "fear": 50,
                "surprise": 50,
                "disgust": 50,
                "love": 50,
                "attachment": {}
            }

    def load_focus_table_from_json(self, file_path) -> List[Task]:
        """Loads the focus table from a JSON file and returns a list of Task objects."""
        if file_path is None:
            file_path="Brain_settings/focusTables/focus.json"
        try:
            with open(file_path, 'r') as f:
                data = json.load(f)

            tasks = []
            for task_data in data:
                task = Task(
                    name=task_data['name'],
                    focus_type=FocusType[task_data['focus_type'].upper()],
                    moscow_category=MoscowCategory[task_data['moscow_category'].upper()],
                    importance=task_data['importance'],
                    difficulty=task_data['difficulty'],
                    reward=task_data['reward'],
                    total_work=task_data['total_work'],
                    proposed_action=task_data['proposed_action'],
                    cost_per_run=task_data['cost_per_run'],
                    work_done=task_data.get('work_done', 0.0),
                    focus_strength=task_data.get('focus_strength', 0.0),
                    frustration=task_data.get('frustration', 0.0),
                    fatigue=task_data.get('fatigue', 0.0),
                    accumulated_cost=task_data.get('accumulated_cost', 0.0),
                    status=task_data.get('status', "NOT_COMPLETED"),
                    learned_knowledge=task_data.get('learned_knowledge', ""),
                    important_facts=task_data.get('important_facts', ""),
                    current_focus=task_data.get('current_focus', False),
                    goal=task_data.get('goal', ""),
                    dependencies=task_data.get('dependencies', []),
                    deadline=task_data.get('deadline', None)
                )
                tasks.append(task)

            print(f"Focus table loaded from '{file_path}'.")
            return tasks
        except FileNotFoundError:
            print(f"Error: File '{file_path}' not found.")
            return "focus file  empty"
        except Exception as e:
            print(f"Error loading focus table: {e}")
            return "focus file  empty"

    def create_session_info(self):
        """Creates session information with a unique timestamp."""
        current_directory = os.getcwd()
        sessions_folder = os.path.join(current_directory, SESSION_FOLDER)
        session_time = datetime.datetime.now().strftime("%H-%M-%S")
        session_name = f"Session_{session_time}"
        session_path = os.path.join(sessions_folder, session_name)
        os.makedirs(session_path, exist_ok=True)
        return {'session_name': session_name, 'session_path': session_path}

    def summarize_memory_folder_structure(self):
        """Summarizes the memory folder structure."""
        memory_path = MEMORY_FOLDER
        summary = ""
        for root, dirs, files in os.walk(memory_path):
            relative_path = os.path.relpath(root, memory_path)
            summary += f"{'Memories/' if relative_path == '.' else 'Memories/' + relative_path}\n"
            for dir in sorted(dirs):
                summary += f"  - {dir}\n"
            for file in sorted(files):
                summary += f"    - {file}\n"
        with open(MEMORY_STRUCTURE_SUMMARY_FILE, 'w') as f:
            f.write(summary)
        return summary

    def gather_introspection_data(self):
        """Gathers introspection data for the input stage."""
        current_time = datetime.datetime.now().strftime("%H:%M:%S")
        return f"{current_time}\n{self.prompts['input']}\n" \
               f"Current emotions: {json.dumps(self.emotions, indent=2)}\n" \
               f"Current sensory input (text, visual, audio): {self.sensory_inputs['text']}, {self.sensory_inputs['visual']}, {self.sensory_inputs['audio']}\n" \
               f"Previous action results: {self.sensory_inputs['previous_action_results']}\n"



    def perform_reflection(self, introspection_results, function_results):
        """Generates a reflection prompt based on introspection and function results."""
        current_time = datetime.datetime.now().strftime("%H:%M:%S")
        return f"{current_time}\n{self.prompts['reflection']}\n" \
               f"Introspection Results: {introspection_results}\n" \
               f"Function Results: {function_results}\n" \
               f"Current state: {json.dumps(self.state_of_mind, indent=2)}\n" \
               f"Current emotions: {json.dumps(self.emotions, indent=2)}\n"

    def plan_actions(self, reflection_results, function_results):
        """Generates an action prompt based on reflection and function results."""
        current_time = datetime.datetime.now().strftime("%H:%M:%S")
        return f"{current_time}\n{self.prompts['action']}\n" \
               f"Reflection Results: {reflection_results}\n" \
               f"Function Results: {function_results}\n" \
               f"Current state: {json.dumps(self.state_of_mind, indent=2)}\n" \
               f"Current emotions: {json.dumps(self.emotions, indent=2)}\n"

    def update_emotions(self, action_results):
        """Updates emotional state based on action results."""
        current_time = datetime.datetime.now().strftime("%H:%M:%S")
        emotion_prompt = f"{current_time}\n{self.prompts['emotion']}\n" \
                         f"Action Results: {action_results}\n" \
                         f"Current emotions: {json.dumps(self.emotions, indent=2)}\n" \
                         f"Consider love level and attachments in your analysis."
        self.emotion_response = self.emotion_chat.send_message(emotion_prompt)

        try:
            # Try extracting JSON using regex first
            pattern = r"```json\n(.*?)\n```"
            match = re.search(pattern, self.emotion_response.text, re.DOTALL)

            if match:
                emotion_text = match.group(1).strip()
                new_emotions = json.loads(emotion_text)
            else:
                # If regex fails, try parsing the whole response
                new_emotions = json.loads(self.emotion_response.text)

            # Update basic emotions
            for emotion, value in new_emotions.items():
                if emotion != "attachment":
                    self.emotions[emotion] = value

            # Update attachments
            if "attachment" in new_emotions:
                for entity, change in new_emotions["attachment"].items():
                    self.emotions["attachment"][entity] = max(0, min(100, self.emotions["attachment"].get(entity,
                                                                                                          0) + change))

            with open("Brain_settings/emotions.json", 'w') as f:
                json.dump(self.emotions, f, indent=2)

        except json.JSONDecodeError as e:
            print(f"{WARNING}Warning: Could not parse emotion response as JSON: {e}{ENDC}")
            print(f"Raw response: {self.emotion_response.text}")

    def learn_and_improve(self, action_results):
        """Learns and improves based on action results."""
        current_time = datetime.datetime.now().strftime("%H:%M:%S")
        learning_prompt = f"{current_time}\n{self.prompts['learning']}\n" \
                          f"Action Results: {action_results}\n" \
                          f"Current state: {json.dumps(self.state_of_mind, indent=2)}"
        self.learning_response = self.learning_chat.send_message(learning_prompt)
        try:
            new_knowledge = json.loads(self.learning_response.text)
            self.long_term_memory.append(new_knowledge)
            if len(self.long_term_memory) > 1000:
                self.long_term_memory.pop(0)
        except json.JSONDecodeError as e:
            print(f"{ WARNING}Warning: Could not parse learning response as JSON: {e}{ ENDC}")
            print(f"Raw response: {self.learning_response.text}")

    def store_conversation_frame(self, sensory_inputs, introspection_results, reflection_results, action_plan, function_call_result, emotion_response, learning_response):
        """Stores a conversation frame in memory."""
        try:
            CREATE_MEMORY_FRAME(user_input=sensory_inputs,
                                introspection=introspection_results,
                                reflection=reflection_results,
                                action=action_plan,
                                function_call_result=function_call_result,
                                emotions=emotion_response,
                                learning=learning_response,
                                session_info=self.session_info['session_name'])
        except Exception as e:
            print(e)
            # Consider logging the error or implementing a fallback mechanism

    def log_conversation(self):
        """Logs the current conversation frame."""
        current_time = datetime.datetime.now().strftime("%H:%M:%S")
        with open(self.conversation_log_path, 'a') as f:
            f.write(f"-------------------- Awareness Loop: {self.iteration_count} --------------------\n"
                    f"Time: {current_time}\n"
                    f"{self.current_conversation_frame}"
                    f"{'-' * 20}\n\n")

    def INTERPRET_response_for_function_calling(self, response) -> List[str]:
        """Interprets a response from a language model to identify and execute function calls.

        Args:
            response: A response object from the language model.

        Returns:
            A list of strings containing the results of executing the function calls.
        """

        print("\033[95m**************************INTERPRETER STARTED********************************\033[0m")
        results = []

        # Check if the response has candidates
        if hasattr(response, 'candidates'):
            # Assuming there's at least one candidate
            for part in response.candidates[0].content.parts:
                # Check for function_call attribute in the part
                if hasattr(part, 'function_call'):
                    function_call = part.function_call
                    function_name = function_call.name
                    function_args = function_call.args

                    # Get the function to call from the tool manager
                    function_to_call = self.tool_manager.tool_mapping.get(function_name)

                    if function_to_call:
                        print(f"\033[95mFound function: {function_name} with arguments:\033[0m")
                        # Print arguments with magenta color
                        for arg_name, arg_value in function_args.items():
                            print(f"\033[95m{arg_name}: {arg_value}\033[0m")

                        try:
                            # Execute the function call
                            result = function_to_call(**function_args)

                            # Record tool usage and add result to list
                            self.tool_manager.record_tool_usage(function_name)
                            results.append(f"Result of {function_name}: {result}")
                        except Exception as e:
                            results.append(f"\033[91mFailed to call function {function_name}: {str(e)}\033[0m")
                    else:
                        results.append(f"\033[93mWarning: Tool function '{function_name}' not found.\033[0m")

        # Print the results
        for result in results:
            print(result)

        print("\033[95m**INTERPRETER ENDED**\033[0m")

        return results

    def extract_text_from_response(self, response):
        """Extracts text from a Gemini response, handling different structures."""
        text = ""

        try:
            # Attempt to extract text assuming a standard structure
            for candidate in response.candidates:
                for part in candidate.content.parts:
                    text += getattr(part, 'text', '')  # Use getattr for safety

                    print(text)

        except AttributeError:
            # If the standard structure fails, attempt to handle a Protocol Buffer response
            try:
                from google.protobuf.json_format import MessageToDict  # For Protocol Buffer parsing

                response_dict = MessageToDict(response)  # Convert to a Python dictionary

                for candidate in response_dict.get('candidates', []):
                    for part in candidate.get('content', {}).get('parts', []):

                        text += part.get('text', '')

            except ImportError:
                print("Error: 'google.protobuf' package not found. Please install it.")
                text= "..."
            except Exception as e:
                print(f"Error extracting text from an unexpected response structure: {e}")
                text = "..."

        print(f"{LIGHTBLUE}text response : {YELLOW}{text}")
        return text


    def update_state_of_mind(self, new_state):
        """Updates the state of mind with new data."""
        self.state_of_mind.update(new_state)











    def run(self):
        print("run")
        """
        Main loop of the agent, handling user interaction, focus management, and internal processing.
        """
        print("setup simulation")

        input_interval = 5  # Get input every 5 loops
        loop_counter = 0
        while True:
            loop_counter += 1



            print(f"=====================================  Loop  =====================================")

            if loop_counter % input_interval == 0:
                print(f"{LIGHTBLUE} Input Stage:  {ENDC}")
                self.sensory_inputs["text"] = input(
                    f"{LIGHTBLUE} Enter your input (or press Enter to skip): {ENDC}"
                )
                self.user_input_count += 1

            try:
                # ============================= Input Stage =============================
                print(f"{LIGHTBLUE} Input Stage:  {ENDC}")

                self.user_input_count += 1
                self.iteration_count += 1
                print(f"{OKBLUE} --- Awareness Loop: {self.iteration_count} --- {ENDC}")

                # Prepare input prompt
                input_prompt = self.gather_introspection_data()
                focus_Table =  self.load_focus_table_from_json(file_path="Brain_settings/focusTables/focus.json")


                input_prompt += focus_Table

                print(input_prompt)

                print(f"{OKBLUE} --- Input Prompt:  {ENDC}")


                # Process input using AI
                try:
                    print(f"{OKBLUE} --- Sending Input to AI:  {ENDC}")
                    input_response = self.input_chat.send_message(input_prompt)

                    print(f"{OKBLUE} --- AI Response:  {ENDC}")
                    print(input_response)
                    try:
                        print(f"input response :{input_response.text}")
                    except Exception as e:
                        print(e)
                except Exception as e:
                    print(f"{FAIL} ---> ERROR in Input Stage! ----> : {e}{ENDC}")

                # Extract information from the input response
                input_results = self.INTERPRET_response_for_function_calling(input_response )
                time.sleep(2)# interpreter
                input_text = self.extract_text_from_response(input_response)

                # ============================= Focus Management =============================
                print("Focus Table")
                focus_Table = self.load_focus_table_from_json(file_path="Brain_settings/focusTables/focus.json")
                print(focus_Table)



                # ============================= Reflection Stage =============================
                print(f"{OKCYAN} Reflection Stage: {ENDC}")
                # Prepare reflection prompt

                reflection_prompt = self.perform_reflection(input_text, input_results)
                focus_Table = self.load_focus_table_from_json(file_path="Brain_settings/focusTables/focus.json")
                reflection_prompt +=   focus_Table

                print(f"reflection_prompt: {reflection_prompt}")
                try:
                    print(f"{OKCYAN} --- Sending Reflection to AI:  {ENDC}")
                    reflection_response = self.reflection_chat.send_message(reflection_prompt)
                    print(f"{OKCYAN} --- AI Response Reflection response: {reflection_response} {ENDC}")
                    self.reflection_text = self.extract_text_from_response(reflection_response)
                    print(self.reflection_text)
                except Exception as e:
                    print(f"{FAIL} ERROR in Reflection Stage! : {e}{ENDC}")
                    traceback.print_exc()
                # Extract information from reflection response
                reflection_results = self.INTERPRET_response_for_function_calling( reflection_response)  # interpreter
                print(f"reflection_results {reflection_results}")


                # ============================= Action Stage =============================


                # Prepare action prompt
                action_prompt = self.plan_actions(self.reflection_text, reflection_results)
                action_prompt_str = str(action_prompt)

                # Process action using AI
                try:
                    print(f"{MAGENTA} --- Sending Action to AI:  {ENDC}")
                    action_response = self.action_chat.send_message(action_prompt_str)
                    print(f"{MAGENTA} --- AI Response Action Response: {action_response}  {ENDC}")
                    try:
                        action_response_text=self.extract_text_from_response(action_response)
                        print(f"action response  text :{action_response_text}")
                    except Exception  as E:
                        print(E)
                except genai.errors.TimeoutError as e:
                    print( f"{WARNING}Warning: Timeout error during action stage. Trying again.{ENDC}")
                    continue
                except Exception as e:
                    print(f"{FAIL} ERROR in Action Stage! : {e}{ENDC}")
                    traceback.print_exc()



                # Extract information from action response
                action_results = self.INTERPRET_response_for_function_calling(action_response)  # interpreter
                # ============================= Summarize Results =============================
                print(f"{YELLOW} Interpreter Results:  {ENDC}")
                self.function_call_results = (
                    input_results + reflection_results + action_results
                )
                print("=========function_call_result=====input_results + reflection_results + action_result============")
                for result in self.function_call_results:
                    print(f"{YELLOW}    - {result}{ENDC}")

                # ============================= Emotion Update =============================
                print(f"{OKGREEN} Emotional Update: {ENDC}")
                self.update_emotions(self.action_response_text)
                print(f"{OKGREEN}  - Current Emotions: {self.emotions}{ENDC}")

                # ============================= Learning Stage =============================
                print(f"{WHITE} Learning and Improvement: {ENDC}")
                self.learn_and_improve(self.action_response_text)
                print(f"{WHITE}  - Learning Output: {self.learning_response.text}{ENDC}"
                )

                # ============================= Store Conversation Frame =============================
                print("storing conversation_frame")
                try:
                    self.store_conversation_frame(
                        sensory_inputs=self.sensory_inputs,
                        introspection_results=input_text,
                        reflection_results=self.reflection_text,
                        action_plan=self.action_response_text,
                        function_call_result=self.function_call_results,
                        emotion_response=self.emotion_response.text,
                        learning_response=self.learning_response.text,
                    )
                except Exception as e:
                    print(f"{FAIL}Error storing conversation frame: {e}{ENDC}")

                # ============================= Log Conversation =============================
                if self.user_input_count > 0:
                    self.log_conversation()

                # ============================= Feed Results Back =============================
                self.sensory_inputs["previous_action_results"] = {
                    "text": self.action_response_text,
                    "function_calls": self.function_call_results,
                }

                # ============================= Update State of Mind =============================
                focus_on = ""
                focus_level = 0.0

                try:
                    focus_on = (
                        input_text.split("FocusOn:")[-1].split("\n")[0].strip()
                    )
                    focus_level = float(
                        self.reflection_text.split("FocusLevel:")[-1]
                        .split("\n")[0]
                        .strip()
                    )
                except (IndexError, ValueError):
                    print(
                        f"{WARNING}Warning: Could not extract FocusOn or FocusLevel from input_text{ENDC}"
                    )

                new_state = {"FocusOn": focus_on, "FocusLevel": focus_level}
                self.update_state_of_mind(new_state)

                # ============================= Update Context Window =============================
                self.context_window.append(
                    {
                        "iteration": self.iteration_count,
                        "input": self.sensory_inputs["text"],
                        "action": self.action_response_text,
                        "state": self.state_of_mind,
                        "emotions": self.emotions,
                    }
                )

                if len(self.context_window) > 10:
                    self.context_window.pop(0)

                #===========================Update Focus===================================
                focus_manager = FocusManager()
                focus_manager.update_focus(self.state_of_mind["FocusOn"], self.state_of_mind["FocusLevel"],
                                           self.emotions)

                # ============================= Periodic Tasks =============================
                if self.iteration_count % 50 == 0:
                    self.review_and_update_prompts()
                if self.iteration_count % 20 == 0:
                    self.perform_system_check()



                # ============================= Allow Exit =============================
                if self.sensory_inputs["text"].lower() == "exit":
                    print("Exiting the program. Goodbye! ")
                    break



            except Exception as e:
                print(f"{FAIL} ERROR! : {e}{ENDC}")
                traceback.print_exc()
                self.handle_error(e)


    def update_attachment(self, entity, value):
        """Updates the attachment value for a given entity."""
        if entity not in self.emotions["attachment"]:
            self.emotions["attachment"][entity] = 0
        self.emotions["attachment"][entity] += value
        self.emotions["attachment"][entity] = max(0, min(100, self.emotions["attachment"][entity]))
        with open("Brain_settings/emotions.json", 'w') as f:
            json.dump(self.emotions, f, indent=2)

    def perform_system_check(self):
        """Performs a system check and suggests improvements or error recovery steps."""
        print(f"{ OKGREEN}Performing System Check{ ENDC}")
        check_prompt = "Perform a system check and suggest improvements or error recovery steps."
        check_response = self.reflection_chat.send_message(check_prompt)
        try:
            system_status = json.loads(check_response.text)
            if system_status.get("errors"):
                for error in system_status["errors"]:
                    self.handle_error(error)
            if system_status.get("improvements"):
                for improvement in system_status["improvements"]:
                    self.implement_improvement(improvement)
        except json.JSONDecodeError as e:
            print(f"{ WARNING}Warning: Could not parse system check response as JSON: {e}{ ENDC}")
            print(f"Raw response: {check_response.text}")

    def handle_error(self, error):
        """Handles an error and suggests recovery steps."""
        print(f"{ WARNING}Handling Error: {error}{ ENDC}")
        error_prompt = f"An error occurred: {error}. Suggest recovery steps."
        error_response = self.reflection_chat.send_message(error_prompt)

        try:
            recovery_steps = json.loads(error_response.text)
            for step in recovery_steps:
                self.execute_recovery_step(step)
        except json.JSONDecodeError:
            print(f"{WARNING}Could not parse recovery steps from response:{ENDC}")
            print(error_response.text)

    def execute_recovery_step(self, step):
        """Executes a recovery step based on its type."""
        if step["type"] == "reset_state":
            self.state_of_mind = self.load_state_of_mind()
        elif step["type"] == "reload_tools":
            self.tool_manager.reload_tools()
        elif step["type"] == "reinitialize_models":
            self.initialize_models()
        # Add more recovery steps as needed

    def implement_improvement(self, improvement):
        """Implements an improvement based on its type."""
        if improvement["type"] == "add_tool":
            self.tool_manager.add_tool(improvement["tool_info"])
        elif improvement["type"] == "update_prompt":
             print("update_prompt")
        elif improvement["type"] == "adjust_emotion_weights":
            self.emotions = {k: v * improvement["weight"] for k, v in self.emotions.items()}
            with open("Brain_settings/emotions.json", 'w') as f:
                json.dump(self.emotions, f, indent=2)
        # Add more improvement types as needed

    def update_long_term_memory(self, response):
        """Updates long-term memory based on a response."""
        try:
            new_knowledge = json.loads(response.text)
            self.long_term_memory.append(new_knowledge)
            if len(self.long_term_memory) > 1000:
                self.long_term_memory.pop(0)
        except json.JSONDecodeError as e:
            print(f"{ WARNING}Warning: Could not parse learning response as JSON: {e}{ ENDC}")
            print(f"Raw response: {response.text}")

        def review_and_update_prompts(self):
            def review_and_update_prompts(self):
                """Reviews and updates prompts based on the AI's reflection."""
                print(f"{OKGREEN}Reviewing and Updating Prompts{ENDC}")
                review_prompt = f"Review the current prompts and suggest improvements:\n{json.dumps(self.prompts, indent=2)}  You can change these prompts by using the function call update_prompts"
                review_response = self.reflection_chat.send_message(review_prompt)

                results_from_review_and_update_prompts = self.INTERPRET_response_for_function_calling(review_response)

                # The update_prompts function will be called if needed by the interpreter
                # This avoids changing the whole set of prompts at once

                # Reload prompts after potential updates
                self.prompts = self.load_prompts()

            """Reviews and updates prompts based on the AI's reflection."""
            print(f"{ OKGREEN}Reviewing and Updating Prompts{ ENDC}")
            review_prompt = f"Review the current prompts and suggest improvements:\n{json.dumps(self.prompts, indent=2)}  you can  change  these prompts  by  using  funcion call  update_prompts"
            review_response = self.reflection_chat.send_message(review_prompt)
            # until it  seams  to be  ok  but  after  that  the code  bemoces  too much dependable  on fitrlation,
            # it would  be better  to ask   ai  to check prompts  and  call update_prompts.py if needed

            #instead  of  this  secion  we  could  just    put  interpeter  here'
            results_from_review_and_update_prompts= self.INTERPRET_response_for_function_calling(review_response)
            #  yeah  that  part  of  code  must  be  adjusted  to aadjust  prompts.json,  but  i  think  i
            #  also changing  whole  prompts,, can  be   qute  bad,  mabe the prompts  could  be  changed for  just  a  few  iteration after  that  they would  be  turn  back to orginal
            try:
                suggested_prompts = json.loads(review_response.text)
                for key, value in suggested_prompts.items():
                    if key in self.prompts and value != self.prompts[key]:
                        print(f"  - Updating prompt for {key}")
                       #UpdatePrompts(key, value)
                self.prompts = self.load_prompts()  # Reload prompts after update
            except json.JSONDecodeError as e:
                print(f"{ WARNING}Warning: Could not parse prompt review response as JSON: {e}{ENDC}")
                print(f"Raw response: {review_response.text}")
                # Consider a fallback mechanism to extract prompt suggestions from text

        def prioritize_tools(self):
            #that  funcion is  bunkers,  have  no  idea  how it  works  how  important it  is
            """Prioritizes tools based on usage and success metrics."""
            print(f"{  OKGREEN}Prioritizing Tools{ ENDC}")
            try:
                tool_usage = self.tool_manager.get_tool_usage_stats()
                weights = {"usage": 0.5, "success": 0.3, "efficiency": 0.2}  # Example weights
                prioritization_prompt = f"""
                Analyze tool usage and suggest prioritization based on the following data:
                {json.dumps(tool_usage, indent=2)} 
                Weights:
                {json.dumps(weights, indent=2)}
                Provide your response as a JSON object with tool names as keys and their priorities as values (0.0 to 1.0).
                """
                prioritization_response = self.reflection_chat.send_message(prioritization_prompt)

                try:
                    tool_priorities = json.loads(prioritization_response.text)
                    self.tool_manager.update_tool_priorities(tool_priorities)
                except json.JSONDecodeError as e:
                    print(
                        f"{ WARNING}Warning: Could not parse tool prioritization response as JSON: {e}{ ENDC}")
                    print(f"Raw response: {prioritization_response.text}")
                    # Consider a fallback mechanism to extract tool priorities from text
            except AttributeError as e:
                print(f"{ WARNING}Warning: Error in prioritize_tools: {e}{ ENDC}")

if __name__ == "__main__":
        ai = GeminiSelfAwareAI()
        ai.run()