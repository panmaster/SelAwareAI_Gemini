import os
import datetime
import json
import google.generativeai as genai
from memory_frame_creation import CREATE_MEMORY_FRAME
from Tool_Manager import ToolManager
import traceback
from SelAwareAI_Gemini.Gemini_SELF_AWARE.PROJECT_8a.tools.AI_related.ChangeOwnState import ChangeOwnState
from SelAwareAI_Gemini.Gemini_SELF_AWARE.PROJECT_8a.tools.AI_related.UpdatePrompts import UpdatePrompts
from FOCUS_1 import FocusManager, FocusType, MoscowCategory



import ast
import re
from termcolor import colored
from typing import Any, Dict, Optional

# Configuration
genai.configure(api_key='AIzaSyA60tGw6fZwQdamW8sm6pkgRh5W559kLJ0')  # Replace with your actual API key
SESSION_FOLDER, MEMORY_FOLDER = "sessions", "memories"
MEMORY_STRUCTURE_SUMMARY_FILE = "memory_structure_summary.txt"

# ANSI escape codes for text colors
class bcolors:
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

    def load_state_of_mind(self):
        """Loads state of mind from Focus.json."""
        try:
            with open("Brain_settings/Focus.json", 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            print(f"{bcolors.WARNING}Warning: Focus.json not found. Using default state of mind.{bcolors.ENDC}")
            return {"FocusOn": "", "FocusLevel": 0.0}

    def load_prompts(self):
        """Loads prompts from prompts.json."""
        try:
            with open("Brain_settings/prompts.json", 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            print(f"{bcolors.WARNING}Warning: prompts.json not found. Using default prompts.{bcolors.ENDC}")
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
            print(f"{bcolors.WARNING}Warning: emotions.json not found. Using default emotions.{bcolors.ENDC}")
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
               f"Current state: {json.dumps(self.state_of_mind, indent=2)}\n" \
               f"Current emotions: {json.dumps(self.emotions, indent=2)}\n" \
               f"Current sensory input (text, visual, audio): {self.sensory_inputs['text']}, {self.sensory_inputs['visual']}, {self.sensory_inputs['audio']}\n" \
               f"Previous action results: {self.sensory_inputs['previous_action_results']}\n"

    def retrieve_Focus(self):
        """Retrieves and displays Focus memory data."""
        try:
            with open("Brain_settings/Focus.json", 'r') as file:
                file_contents = file.read()
                try:
                    parsed_data = json.loads(file_contents)
                    FocusData = json.dumps(parsed_data)
                except json.JSONDecodeError:
                    FocusData = file_contents
            return f"Focus Memory Data: {FocusData}"
        except FileNotFoundError:
            return "Focus Memory Data: Not Found"

    def Set_Focus(self, focus_on=None):
        """Sets the focus in the Focus.json file."""
        try:
            # Load existing data
            with open("Brain_settings/Focus.json", 'r') as file:
                data = json.load(file)
        except FileNotFoundError:
            data = {}

        if focus_on:
            data["FocusOn"] = focus_on

        # Save updated data
        with open("Brain_settings/Focus.json", 'w') as file:
            json.dump(data, file, indent=4)

        return f"Focus set to: {focus_on}"

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
                    self.emotions["attachment"][entity] = max(0, min(100, self.emotions["attachment"].get(entity, 0) + change))

            with open("Brain_settings/emotions.json", 'w') as f:
                json.dump(self.emotions, f, indent=2)

        except json.JSONDecodeError as e:
            print(f"{bcolors.WARNING}Warning: Could not parse emotion response as JSON: {e}{bcolors.ENDC}")
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
            print(f"{bcolors.WARNING}Warning: Could not parse learning response as JSON: {e}{bcolors.ENDC}")
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
            print(f"{bcolors.FAIL}Error storing conversation frame: {e}{bcolors.ENDC}")
            # Consider logging the error or implementing a fallback mechanism

    def log_conversation(self):
        """Logs the current conversation frame."""
        current_time = datetime.datetime.now().strftime("%H:%M:%S")
        with open(self.conversation_log_path, 'a') as f:
            f.write(f"-------------------- Awareness Loop: {self.iteration_count} --------------------\n"
                    f"Time: {current_time}\n"
                    f"{self.current_conversation_frame}"
                    f"{'-' * 20}\n\n")

    def interpret_response_for_function_calling(self, response):
        """Interprets the response for function calls."""
        print("********************************************INTERPRETER*******************************************")
        results = []

        def process_function_call(function_call):
            """Processes a function call and executes it."""
            function_name = function_call.name
            function_args = function_call.args
            function_to_call = self.tool_manager.tool_mapping.get(function_name)
            if function_to_call:
                try:
                    result = function_to_call(**function_args)
                    self.tool_manager.record_tool_usage(function_name)
                    results.append(f"Result of {function_name}: {result}")
                except Exception as e:
                    results.append(f"{bcolors.FAIL}Failed to call function {function_name}: {str(e)}{bcolors.ENDC}")
            else:
                results.append(f"{bcolors.WARNING}Warning: Tool function '{function_name}' not found.{bcolors.ENDC}")

        def process_content(content):
            """Processes the content of a response, looking for function calls."""
            if hasattr(content, 'parts'):
                for part in content.parts:
                    if hasattr(part, 'function_call'):
                        process_function_call(part.function_call)
            elif hasattr(content, 'function_call'):
                process_function_call(content.function_call)

        if hasattr(response, 'result'):
            response = response.result

        if hasattr(response, 'candidates'):
            for candidate in response.candidates:
                if hasattr(candidate, 'content'):
                    process_content(candidate.content)
        elif hasattr(response, 'content'):
            process_content(response.content)
        elif isinstance(response, dict):
            if 'candidates' in response:
                for candidate in response['candidates']:
                    if 'content' in candidate:
                        process_content(candidate['content'])
            elif 'content' in response:
                process_content(response['content'])

        return results

    def initialize_models(self):
        """Initializes the Gemini models for different stages."""
        try:
            alltools_str = self.tool_manager.get_tools_list_json("all")
            input_tools_str = self.tool_manager.get_tools_list_json("input")

            alltools = ast.literal_eval(alltools_str)
            input_tools = ast.literal_eval(input_tools_str)

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

            self.input_model = genai.GenerativeModel(
                system_instruction=input_instruction,
                model_name="gemini-1.5-flash-latest",
                tools=input_tools)
            self.input_chat = self.input_model.start_chat(history=[])

            self.reflection_model = genai.GenerativeModel(
                system_instruction=reflection_instruction,
                model_name="gemini-1.5-flash-latest",
                safety_settings={"HARASSMENT": "block_none"},
                tools=alltools)
            self.reflection_chat = self.reflection_model.start_chat(history=[])

            self.action_model = genai.GenerativeModel(
                system_instruction=action_instruction,
                model_name="gemini-1.5-flash-latest",
                safety_settings={"HARASSMENT": "block_none"},
                tools=alltools)
            self.action_chat = self.action_model.start_chat(history=[])

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

            print(f"{bcolors.OKGREEN}Models initialized successfully!{bcolors.ENDC}")
        except Exception as E:
            raise RuntimeError(f"{bcolors.FAIL}Error initializing models: {E}{bcolors.ENDC}")

    def extract_text_from_response(self, response):
        """Extracts text from a Gemini response."""
        text = ""
        for candidate in response.candidates:
            for part in candidate.content.parts:
                if hasattr(part, 'text'):
                    text += part.text
        return text

    def update_state_of_mind(self, new_state):
        """Updates the state of mind with new data."""
        self.state_of_mind.update(new_state)
        ChangeOwnState(**new_state)




    def run(self):

        self.focus_manager = FocusManager()
        #  Add your initial FocusPoints
        self.focus_manager.add_focus_point("UnderstandUserNeeds", FocusType.GOAL_ORIENTED, MoscowCategory.MUST, 1.0,
                                           0.8, 1.0, 100,
                                           "Analyze user input", 10)
        """The main loop of the self-aware AI."""



          # Select an initial focus point before the



        while True:
            try:
                # Prepare for next iteration
                self.sensory_inputs["text"] = input(
                    f"{bcolors.LIGHTBLUE}🎙️  Enter your input (or press Enter to skip): {bcolors.ENDC}")
                self.user_input_count += 1

                self.iteration_count += 1
                print(f"{bcolors.OKBLUE}✨🧠--- Awareness Loop: {self.iteration_count} ---🧠✨{bcolors.ENDC}")

                # Input stage
                print(f"{bcolors.LIGHTBLUE}📥 Input Stage:{bcolors.ENDC}")
                input_prompt = self.gather_introspection_data()
                input_prompt += self.retrieve_Focus()
                try:
                    input_response = self.input_chat.send_message(input_prompt)
                except genai.errors.TimeoutError as e:
                    print(f"{bcolors.WARNING}Warning: Timeout error during input stage. Trying again.{bcolors.ENDC}")
                    # Implement a retry mechanism here
                    continue  # Skip to the next iteration
                except Exception as e:
                    print(f"{bcolors.FAIL}🚨  ERROR in Input Stage!  🚨: {e}{bcolors.ENDC}")
                    traceback.print_exc()
                    # Implement a recovery mechanism (reset, reinitialize, etc.)
                    continue  # Skip to the next iteration

                input_results = self.interpret_response_for_function_calling(input_response)
                input_text = self.extract_text_from_response(input_response)
                print(f"{bcolors.LIGHTBLUE}  - 🤖 Input Response: {input_text}{bcolors.ENDC}")


                #focus
                self.focus_manager.process_stimulus(stimulus_strength=0.5)  # Adjust strength as needed
                self.focus_manager.select_focus()
                current_focus_name = self.focus_manager.current_focus.name
                print(f"{bcolors.OKCYAN}🤔 Current Focus: {current_focus_name}{bcolors.ENDC}")











                # Reflection stage
                print(f"{bcolors.OKCYAN}🤔 Reflection Stage:{bcolors.ENDC}")
                reflection_prompt = self.perform_reflection(input_text, input_results)
                reflection_prompt += f"The current focus is: {current_focus_name}. "
                reflection_prompt += self.retrieve_Focus()  #focus
                try:
                    reflection_response = self.reflection_chat.send_message(reflection_prompt)
                except genai.errors.TimeoutError as e:
                    print(f"{bcolors.WARNING}Warning: Timeout error during reflection stage. Trying again.{bcolors.ENDC}")
                    # Implement a retry mechanism here
                    continue  # Skip to the next iteration
                except Exception as e:
                    print(f"{bcolors.FAIL}🚨  ERROR in Reflection Stage!  🚨: {e}{bcolors.ENDC}")
                    traceback.print_exc()
                    # Implement a recovery mechanism (reset, reinitialize, etc.)
                    continue  # Skip to the next iteration

                reflection_results = self.interpret_response_for_function_calling(reflection_response)
                self.reflection_text = self.extract_text_from_response(reflection_response)
                print(f"{bcolors.OKCYAN}  - 🤖 Reflection Output: {self.reflection_text}{bcolors.ENDC}")

                # Action stage
                print(f"{bcolors.MAGENTA}🚀 Action Stage:{bcolors.ENDC}")
                action_prompt = self.plan_actions(self.reflection_text, reflection_results)
                action_prompt += self.retrieve_Focus()
                try:
                    action_response = self.action_chat.send_message(action_prompt)
                except genai.errors.TimeoutError as e:
                    print(f"{bcolors.WARNING}Warning: Timeout error during action stage. Trying again.{bcolors.ENDC}")
                    # Implement a retry mechanism here
                    continue  # Skip to the next iteration
                except Exception as e:
                    print(f"{bcolors.FAIL}🚨  ERROR in Action Stage!  🚨: {e}{bcolors.ENDC}")
                    traceback.print_exc()
                    # Implement a recovery mechanism (reset, reinitialize, etc.)
                    continue  # Skip to the next iteration

                action_results = self.interpret_response_for_function_calling(action_response)
                self.action_response_text = self.extract_text_from_response(action_response)
                print(f"{bcolors.MAGENTA}  - 🤖 Action Plan: {self.action_response_text}{bcolors.ENDC}")

                print(f"{bcolors.YELLOW}📋 Interpreter Results:{bcolors.ENDC}")
                self.function_call_results = input_results + reflection_results + action_results
                for result in self.function_call_results:
                    print(f"{bcolors.YELLOW}    - ✅ {result}{bcolors.ENDC}")

                # Emotion update
                print(f"{bcolors.OKGREEN}😊 Emotional Update:{bcolors.ENDC}")
                self.update_emotions(self.action_response_text)
                print(f"{bcolors.OKGREEN}  - Current Emotions: {self.emotions}{bcolors.ENDC}")

                # Learning stage
                print(f"{bcolors.WHITE}📚 Learning and Improvement:{bcolors.ENDC}")
                self.learn_and_improve(self.action_response_text)
                print(f"{bcolors.WHITE}  - Learning Output: {self.learning_response.text}{bcolors.ENDC}")

                # Store conversation frame
                try:
                    self.store_conversation_frame(
                        sensory_inputs=self.sensory_inputs,
                        introspection_results=input_text,
                        reflection_results=self.reflection_text,
                        action_plan=self.action_response_text,
                        function_call_result=self.function_call_results,
                        emotion_response=self.emotion_response.text,
                        learning_response=self.learning_response.text
                    )
                except Exception as e:
                    print(f"{bcolors.FAIL}Error storing conversation frame: {e}{bcolors.ENDC}")
                    # Consider logging the error or implementing a fallback mechanism

                # Log conversation
                if self.user_input_count > 0:
                    self.log_conversation()

                # Feed results back into input for next iteration
                self.sensory_inputs["previous_action_results"] = {
                    "text": self.action_response_text,
                    "function_calls": self.function_call_results
                }

                # Update state of mind
                focus_on = ""
                focus_level = 0.0
                try:
                    focus_on = input_text.split("FocusOn:")[-1].split("\n")[0].strip()
                    focus_level = float(self.reflection_text.split("FocusLevel:")[-1].split("\n")[0].strip())
                except (IndexError, ValueError):
                    print(f"{bcolors.WARNING}Warning: Could not extract FocusOn or FocusLevel from input_text{bcolors.ENDC}")

                new_state = {
                    "FocusOn": focus_on,
                    "FocusLevel": focus_level,
                }
                self.update_state_of_mind(new_state)

                # Update context window
                self.context_window.append({
                    "iteration": self.iteration_count,
                    "input": self.sensory_inputs["text"],
                    "action": self.action_response_text,
                    "state": self.state_of_mind,
                    "emotions": self.emotions
                })
                if len(self.context_window) > 10:
                    self.context_window.pop(0)

                # Periodic tasks
                if self.iteration_count % 50 == 0:
                    self.review_and_update_prompts()
                if self.iteration_count % 20 == 0:
                    self.perform_system_check()

                self.self.tool_manager.prioritize_tools(self.reflection_chat)

                # Allow for graceful exit
                if self.sensory_inputs["text"].lower() == "exit":
                    print("Exiting the program. Goodbye! 👋")
                    break


            except Exception as e:

                print(f"{bcolors.FAIL}🚨  ERROR!  🚨: {e}{bcolors.ENDC}")

                traceback.print_exc()

                self.handle_error(e)  # Now, this call will find the

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
        print(f"{bcolors.OKGREEN}Performing System Check{bcolors.ENDC}")
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
            print(f"{bcolors.WARNING}Warning: Could not parse system check response as JSON: {e}{bcolors.ENDC}")
            print(f"Raw response: {check_response.text}")

    def handle_error(self, error):
        """Handles an error and suggests recovery steps."""
        print(f"{bcolors.WARNING}Handling Error: {error}{bcolors.ENDC}")
        error_prompt = f"An error occurred: {error}. Suggest recovery steps."
        error_response = self.reflection_chat.send_message(error_prompt)

        try:
            recovery_steps = json.loads(error_response.text)
            for step in recovery_steps:
                self.execute_recovery_step(step)
        except json.JSONDecodeError:
            print(f"{bcolors.WARNING}Could not parse recovery steps from response:{bcolors.ENDC}")
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
            UpdatePrompts(improvement["prompt_key"], improvement["new_prompt"])
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
            print(f"{bcolors.WARNING}Warning: Could not parse learning response as JSON: {e}{bcolors.ENDC}")
            print(f"Raw response: {response.text}")

        def review_and_update_prompts(self):
            """Reviews and updates prompts based on the AI's reflection."""
            print(f"{bcolors.OKGREEN}Reviewing and Updating Prompts{bcolors.ENDC}")
            review_prompt = f"Review the current prompts and suggest improvements:\n{json.dumps(self.prompts, indent=2)}"
            review_response = self.reflection_chat.send_message(review_prompt)
            try:
                suggested_prompts = json.loads(review_response.text)
                for key, value in suggested_prompts.items():
                    if key in self.prompts and value != self.prompts[key]:
                        print(f"  - Updating prompt for {key}")
                        UpdatePrompts(key, value)
                self.prompts = self.load_prompts()  # Reload prompts after update
            except json.JSONDecodeError as e:
                print(f"{bcolors.WARNING}Warning: Could not parse prompt review response as JSON: {e}{bcolors.ENDC}")
                print(f"Raw response: {review_response.text}")
                # Consider a fallback mechanism to extract prompt suggestions from text

        def prioritize_tools(self):
            """Prioritizes tools based on usage and success metrics."""
            print(f"{bcolors.OKGREEN}Prioritizing Tools{bcolors.ENDC}")
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
                        f"{bcolors.WARNING}Warning: Could not parse tool prioritization response as JSON: {e}{bcolors.ENDC}")
                    print(f"Raw response: {prioritization_response.text}")
                    # Consider a fallback mechanism to extract tool priorities from text
            except AttributeError as e:
                print(f"{bcolors.WARNING}Warning: Error in prioritize_tools: {e}{bcolors.ENDC}")

if __name__ == "__main__":
        ai = GeminiSelfAwareAI()
        ai.run()