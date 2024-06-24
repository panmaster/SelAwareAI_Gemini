import os
import datetime
import json
import google.generativeai as genai
from MEMORY______________frame_creation import CREATE_MEMORY_FRAME
from Tool_Manager import ToolManager
import traceback
from SelAwareAI_Gemini.Gemini_SELF_AWARE.PROJECT_7.tools.AI_related.ChangeOwnState import ChangeOwnState
from SelAwareAI_Gemini.Gemini_SELF_AWARE.PROJECT_6.tools.Cathegory_Os.UpdatePrompts import UpdatePrompts
from SelAwareAI_Gemini.Gemini_SELF_AWARE.PROJECT_7.tools.AI_related.RETRIEVE_RELEVANT_FRAMES import RETRIEVE_RELEVANT_FRAMES
import re
import ast
import asyncio

# Configuration
genai.configure(api_key='AIzaSyA60tGw6fZwQdamW8sm6pkgRh5W559kLJ0')  # Replace with your actual API key
SESSION_FOLDER, MEMORY_FOLDER = "sessions", "memories"
MEMORY_STRUCTURE_SUMMARY_FILE = "memory_structure_summary.txt"
PROMPTS_FILE = os.path.join("Brain_settings", "prompts.json")
EMOTIONS_FILE = os.path.join("Brain_settings", "emotions.json")

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
        self.initialize_models()
        self.initialize()  # Call initialize here
        self.valid_tool_types = {"all", "input", "reflection", "action", "web", "emotions"}

    def initialize(self):
        self.state_of_mind = self.load_state_of_mind()
        self.prompts = self.load_prompts()
        self.emotions = self.load_emotions()

    def load_state_of_mind(self):
        script_dir = os.path.dirname(os.path.abspath(__file__))
        path = os.path.abspath(os.path.join(script_dir, 'Brain_settings/State_of_mind.json'))
        try:
            with open(path, 'r') as f:
                return json.load(f)
        except Exception as E:
            print(f"{bcolors.FAIL}Error loading state of mind: {E}{bcolors.ENDC}")
            return {}

    def load_prompts(self):
        try:
            with open(PROMPTS_FILE, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            default_prompts = {
                "input": "Analyze current inputs, state, and emotions. What's the most important aspect to focus on?  You can call the 'retrieve_memories' function to access past relevant memories.  Provide your response in the following format:\n FocusOn: [identified focus]\n FocusLevel: [a float between 0 and 1]",
                "reflection": "Reflect on recent actions, outcomes, and emotional states. What insights can be drawn? Consider potential improvements or adjustments to behavior and decision-making.  You can also call the 'retrieve_memories' function to access relevant memories.  Format your response to be clear and structured, highlighting key observations and recommendations.",
                "action": "Based on the current focus, reflections, and emotional state, what is the optimal next action? If necessary, use available tools to perform actions.  Always justify your chosen action and explain its expected impact. You can also call the 'retrieve_memories' function to access relevant memories.",
                "emotion": "Based on recent events and outcomes, how should my emotional state be adjusted?  Provide your response as a JSON object with emotion names as keys and values between 0 and 100, representing the intensity of each emotion.",
                "learning": "What new knowledge or skills should be prioritized for long-term improvement based on recent experiences and outcomes? Summarize your insights and recommendations in a concise, structured format that can be easily integrated into the AI's knowledge base."
            }
            self.save_json(PROMPTS_FILE, default_prompts)
            return default_prompts

    def load_emotions(self):
        try:
            with open(EMOTIONS_FILE, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            default_emotions = {
                "happiness": 50,
                "sadness": 50,
                "anger": 50,
                "fear": 50,
                "surprise": 50,
                "disgust": 50
            }
            self.save_json(EMOTIONS_FILE, default_emotions)
            return default_emotions

    def save_json(self, file_path, data):
        with open(file_path, 'w') as f:
            json.dump(data, f, indent=2)

    def create_session_info(self):
        current_directory = os.getcwd()
        sessions_folder = os.path.join(current_directory, "SESSIONS")
        session_time = datetime.datetime.now().strftime("%H-%M-%S")
        session_name = f"Session_{session_time}"
        session_path = os.path.join(sessions_folder, session_name)
        os.makedirs(session_path, exist_ok=True)
        return {'session_name': session_name, 'session_path': session_path}

    def summarize_memory_folder_structure(self):
        memory_path = MEMORY_FOLDER
        summary = ""
        for root, dirs, files in os.walk(memory_path):
            relative_path = os.path.relpath(root, memory_path)
            summary += f"{'Memories/' if relative_path == '.' else 'Memories/' + relative_path}\n"
            for dir in sorted(dirs):
                summary += f"  - {dir}\n"
            for file in sorted(files):
                summary += f"    - {file}\n"
        self.save_json(MEMORY_STRUCTURE_SUMMARY_FILE, summary)
        return summary

    async def gather_introspection_data(self):
        current_time = datetime.datetime.now().strftime("%H:%M:%S")
        return f"{current_time}\n{self.prompts['input']}\n" \
               f"Current state: {json.dumps(self.state_of_mind, indent=2)}\n" \
               f"Current emotions: {json.dumps(self.emotions, indent=2)}\n" \
               f"Current sensory input: {self.sensory_inputs}\n" \
               f"Previous action results: {self.sensory_inputs['previous_action_results']}\n"

    async def retrieve_memories(self, focus_on=None):
        """Retrieves relevant memories based on the current focus."""
        if focus_on:
            relevant_memories = await RETRIEVE_RELEVANT_FRAMES(focus_on)
            return f"Relevant memories: {json.dumps(relevant_memories, indent=2)}"
        return ""

    def perform_reflection(self, introspection_results, function_results):
        current_time = datetime.datetime.now().strftime("%H:%M:%S")
        return f"{current_time}\n{self.prompts['reflection']}\n" \
               f"Introspection Results: {introspection_results}\n" \
               f"Function Results: {function_results}\n" \
               f"Current state: {json.dumps(self.state_of_mind, indent=2)}\n" \
               f"Current emotions: {json.dumps(self.emotions, indent=2)}\n"

    def plan_actions(self, reflection_results, function_results):
        current_time = datetime.datetime.now().strftime("%H:%M:%S")
        return f"{current_time}\n{self.prompts['action']}\n" \
               f"Reflection Results: {reflection_results}\n" \
               f"Function Results: {function_results}\n" \
               f"Current state: {json.dumps(self.state_of_mind, indent=2)}\n" \
               f"Current emotions: {json.dumps(self.emotions, indent=2)}\n"

    def update_emotions(self, action_results):
        current_time = datetime.datetime.now().strftime("%H:%M:%S")
        emotion_prompt = f"{current_time}\n{self.prompts['emotion']}\n" \
                         f"Action Results: {action_results}\n" \
                         f"Current emotions: {json.dumps(self.emotions, indent=2)}"
        emotion_response = self.emotion_chat.send_message(emotion_prompt)

        try:
            # Regular expression pattern for extracting the JSON data
            pattern = r"```json\n(.*?)\n```"
            match = re.search(pattern, emotion_response.text)

            if match:
                emotion_text = match.group(1).strip()  # Extract the JSON data
                new_emotions = json.loads(emotion_text)
                self.emotions.update(new_emotions)
                self.save_json(EMOTIONS_FILE, self.emotions)
            else:
                print(f"{bcolors.WARNING}Warning: Could not find valid JSON data in the response.{bcolors.ENDC}")
                print(f"Raw response: {emotion_response.text}")

        except json.JSONDecodeError as e:
            print(f"{bcolors.WARNING}Warning: Could not parse emotion response as JSON: {e}{bcolors.ENDC}")
            print(f"Raw response: {emotion_response.text}")

    def learn_and_improve(self, action_results):
        current_time = datetime.datetime.now().strftime("%H:%M:%S")
        learning_prompt = f"{current_time}\n{self.prompts['learning']}\n" \
                          f"Action Results: {action_results}\n" \
                          f"Current state: {json.dumps(self.state_of_mind, indent=2)}"
        learning_response = self.learning_chat.send_message(learning_prompt)
        try:
            new_knowledge = json.loads(learning_response.text)
            self.long_term_memory.append(new_knowledge)
            if len(self.long_term_memory) > 1000:  # Limit long-term memory size
                self.long_term_memory.pop(0)
        except json.JSONDecodeError as e:
            print(f"{bcolors.WARNING}Warning: Could not parse learning response as JSON: {e}{bcolors.ENDC}")
            print(f"Raw response: {learning_response.text}")

    def store_conversation_frame(self, introspection_results, reflection_results, action_plan, function_results):
        current_conversation_frame = (
            f"Introspection:\n{introspection_results}\n"
            f"Reflection:\n{reflection_results}\n"
            f"Action Plan:\n{action_plan}\n"
            f"Function Call Results:\n{function_results}\n"
        )
        CREATE_MEMORY_FRAME(current_conversation_frame, self.session_info['session_name'])

    def log_conversation(self):
        current_time = datetime.datetime.now().strftime("%H:%M:%S")
        with open(self.conversation_log_path, 'a') as f:
            f.write(f"--- Awareness Loop: {self.iteration_count} ---\n"
                    f"Time: {current_time}\n"
                    f"{self.current_conversation_frame}"
                    f"{'-' * 20}\n\n")

    async def interpret_response_for_function_calling(self, response):
        print("********************************************INTERPRETER*******************************************")
        results = []

        async def process_function_call(function_call):
            function_name = function_call.name
            function_args = function_call.args
            function_to_call = self.tool_manager.tool_mapping.get(function_name)
            if function_to_call:
                try:
                    result = await function_to_call(**function_args)
                    self.tool_manager.record_tool_usage(function_name)  # Record usage
                    results.append(f"Result of {function_name}: {result}")
                except Exception as e:
                    results.append(f"{bcolors.FAIL}Failed to call function {function_name}: {str(e)}{bcolors.ENDC}")
            else:
                results.append(f"{bcolors.WARNING}Warning: Tool function '{function_name}' not found.{bcolors.ENDC}")

        async def process_content(content):
            if hasattr(content, 'parts'):
                for part in content.parts:
                    if hasattr(part, 'function_call'):
                        await process_function_call(part.function_call)
            elif hasattr(content, 'function_call'):
                await process_function_call(content.function_call)

        if hasattr(response, 'result'):
            response = response.result

        if hasattr(response, 'candidates'):
            for candidate in response.candidates:
                if hasattr(candidate, 'content'):
                    await process_content(candidate.content)
        elif hasattr(response, 'content'):
            await process_content(response.content)
        elif isinstance(response, dict):
            if 'candidates' in response:
                for candidate in response['candidates']:
                    if 'content' in candidate:
                        await process_content(candidate['content'])
            elif 'content' in response:
                await process_content(response['content'])

        return results

    def initialize_models(self):
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
        text = ""
        for candidate in response.candidates:
            for part in candidate.content.parts:
                if hasattr(part, 'text'):
                    text += part.text
        return text

    def update_state_of_mind(self, new_state):
        self.state_of_mind.update(new_state)
        ChangeOwnState(**new_state) # No await needed

    async def run(self):
        while True:
            try:
                self.iteration_count += 1
                print(f"{bcolors.OKBLUE}✨🧠--- Awareness Loop: {self.iteration_count} ---🧠✨{bcolors.ENDC}")

                # User input (every other iteration)
                if self.iteration_count % 2 == 1:
                    self.sensory_inputs["text"] = input("🎙️  Enter your input (or press Enter to skip): ")
                    self.user_input_count += 1
                else:
                    self.sensory_inputs["text"] = ""

                print(
                    f"{bcolors.OKCYAN}-----------------------------------INPUT--------------------------------------{bcolors.ENDC}")
                # Input stage
                print(f"{bcolors.HEADER}📥 Input Stage:{bcolors.ENDC}")
                input_prompt = await self.gather_introspection_data()
                input_prompt += await self.retrieve_memories(self.state_of_mind['FocusOn']) # Add memories if needed
                input_response = self.input_chat.send_message(input_prompt)
                input_results = await self.interpret_response_for_function_calling(input_response)
                print(f"  - 🎤 User Input: {self.sensory_inputs['text']}")
                print(f"  - 🎯 Focus: {self.state_of_mind['FocusOn']}")

                input_text = self.extract_text_from_response(input_response)
                print(f"  - 🤖 Input Response: {input_text}")

                print(
                    f"{bcolors.OKCYAN}----------------------------------END INPUT----------------------------------{bcolors.ENDC}")
                print()

                print(
                    f"{bcolors.OKGREEN}-------------------------------- REFLECTION----------------------------------{bcolors.ENDC}")
                # Reflection stage
                print(f"{bcolors.HEADER}🤔 Reflection Stage:{bcolors.ENDC}")

                reflection_prompt = self.perform_reflection(input_text, input_results)
                reflection_prompt += await self.retrieve_memories()  # Add memories if needed
                reflection_response = self.reflection_chat.send_message(reflection_prompt)
                reflection_results = await self.interpret_response_for_function_calling(reflection_response)

                reflection_text = self.extract_text_from_response(reflection_response)
                print(f"  - 🤖 Reflection Output: {reflection_text}")

                print(
                    f"{bcolors.OKGREEN}---------------------------------END REFLECTION--------------------------{bcolors.ENDC}")
                print()

                print(
                    f"{bcolors.WARNING}-------------------------------------ACTION-------------------------------{bcolors.ENDC}")
                # Action stage
                print(f"{bcolors.HEADER}🚀 Action Stage:{bcolors.ENDC}")

                action_prompt = self.plan_actions(reflection_text, reflection_results)
                action_prompt += await self.retrieve_memories()  # Add memories if needed
                action_response = self.action_chat.send_message(action_prompt)
                action_results = await self.interpret_response_for_function_calling(action_response)

                self.action_response_text = self.extract_text_from_response(action_response)
                print(f"  - 🤖 Action Plan: {self.action_response_text}")

                # Combine all results
                print(
                    f"{bcolors.WARNING}-------------------------------------RESULTS-------------------------------{bcolors.ENDC}")
                print(f"{bcolors.HEADER}📋 Results:{bcolors.ENDC}")
                self.function_call_results = input_results + reflection_results + action_results
                for result in self.function_call_results:
                    print(f"    - ✅ {result}")

                # Update emotions
                print(
                    f"{bcolors.OKGREEN}-------------------------------- EMOTIONS ----------------------------------{bcolors.ENDC}")
                print(f"{bcolors.HEADER}😊 Emotional Update:{bcolors.ENDC}")
                self.update_emotions(self.action_response_text)
                print(f"  - Current Emotions: {self.emotions}")

                # Learn and improve
                print(
                    f"{bcolors.OKCYAN}-------------------------------- LEARNING ----------------------------------{bcolors.ENDC}")
                print(f"{bcolors.HEADER}📚 Learning and Improvement:{bcolors.ENDC}")
                self.learn_and_improve(self.action_response_text)

                # Store conversation frame
                self.store_conversation_frame(
                    input_text,
                    reflection_text,
                    self.action_response_text,
                    self.function_call_results
                )

                # Log conversation
                if self.user_input_count > 0:
                    self.log_conversation()

                # Feed action results back into the input for the next iteration
                self.sensory_inputs["previous_action_results"] = {
                    "text": self.action_response_text,
                    "function_calls": self.function_call_results
                }

                # Update state of mind based on action results
                focus_on = ""
                focus_level = 0.0
                try:
                    focus_on = input_text.split("FocusOn:")[-1].split("\n")[0].strip()
                    focus_level = float(input_text.split("FocusLevel:")[-1].split("\n")[0].strip())
                except (IndexError, ValueError):
                    print(
                        f"{bcolors.WARNING}Warning: Could not extract FocusOn or FocusLevel from input_text{bcolors.ENDC}")

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

                # Self-improvement: Periodically review and update prompts
                if self.iteration_count % 50 == 0:
                    self.review_and_update_prompts()

                # Dynamic tool prioritization
                self.prioritize_tools()

                # Error recovery and robustness check
                if self.iteration_count % 20 == 0:
                    self.perform_system_check()

                # Allow for graceful exit
                if self.sensory_inputs["text"].lower() == "exit":
                    print("Exiting the program. Goodbye! 👋")
                    break

            except KeyboardInterrupt:
                print("\nKeyboard interrupt received. Exiting the program. Goodbye! 👋")
                break
            except Exception as e:
                print(f"{bcolors.FAIL}🚨  ERROR!  🚨: {e}{bcolors.ENDC}")
                traceback.print_exc()
                # Pass the exception to handle_error
                await self.handle_error(e)

    def review_and_update_prompts(self):
        print(f"{bcolors.OKGREEN}Reviewing and Updating Prompts{bcolors.ENDC}")
        review_prompt = f"Review the current prompts and suggest improvements:\n{json.dumps(self.prompts, indent=2)}"
        review_response = self.reflection_chat.send_message(review_prompt) # No await needed
        try:
            suggested_prompts = json.loads(review_response.text)
            for key, value in suggested_prompts.items():
                if key in self.prompts and value != self.prompts[key]:
                    print(f"  - Updating prompt for {key}")
                    UpdatePrompts(key, value) # No await needed
            self.prompts = self.load_prompts()  # Reload prompts after update
        except json.JSONDecodeError as e:
            print(f"{bcolors.WARNING}Warning: Could not parse prompt review response as JSON: {e}{bcolors.ENDC}")
            print(f"Raw response: {review_response.text}")

    def prioritize_tools(self):
        print(f"{bcolors.OKGREEN}Prioritizing Tools{bcolors.ENDC}")
        try:
            tool_usage = self.tool_manager.get_tool_usage_stats()
            prioritization_prompt = f"Analyze tool usage and suggest prioritization:\n{json.dumps(tool_usage, indent=2)}"
            prioritization_response = self.reflection_chat.send_message(prioritization_prompt)
            try:
                tool_priorities = json.loads(prioritization_response.text)
                self.tool_manager.update_tool_priorities(tool_priorities)
            except json.JSONDecodeError as e:
                print(
                    f"{bcolors.WARNING}Warning: Could not parse tool prioritization response as JSON: {e}{bcolors.ENDC}")
                print(f"Raw response: {prioritization_response.text}")
        except AttributeError as e:
            print(f"{bcolors.WARNING}Warning: Error in prioritize_tools: {e}{bcolors.ENDC}")

    def perform_system_check(self):
        print(f"{bcolors.OKGREEN}Performing System Check{bcolors.ENDC}")
        check_prompt = "Perform a system check and suggest improvements or error recovery steps."
        check_response = self.reflection_chat.send_message(check_prompt) # No await needed
        try:
            system_status = json.loads(check_response.text)
            if system_status.get("errors"):
                for error in system_status["errors"]:
                    self.handle_error(error) # No await needed
            if system_status.get("improvements"):
                for improvement in system_status["improvements"]:
                    self.implement_improvement(improvement) # No await needed
        except json.JSONDecodeError as e:
            print(f"{bcolors.WARNING}Warning: Could not parse system check response as JSON: {e}{bcolors.ENDC}")
            print(f"Raw response: {check_response.text}")

    async def handle_error(self, error):
        print(f"{bcolors.WARNING}Handling Error: {error}{bcolors.ENDC}")
        error_prompt = f"An error occurred: {error}. Suggest recovery steps."
        error_response = self.reflection_chat.send_message(error_prompt)
        try:
            # Extract text from a potential complex response
            if hasattr(error_response, 'result'):
                error_response = error_response.result
                if 'content' in error_response and 'parts' in error_response['content']:
                    recovery_steps = []
                    for part in error_response['content']['parts']:
                        if 'text' in part:
                            recovery_steps.append(part['text'])
                else:
                    print(f"{bcolors.WARNING}Warning: Error response does not have content or parts.{bcolors.ENDC}")
                    recovery_steps = []
            else:
                print(f"{bcolors.WARNING}Warning: Error response does not have result.{bcolors.ENDC}")
                recovery_steps = []

            for step in recovery_steps:
                try:
                    await self.execute_recovery_step(step)
                except Exception as e:
                    print(f"{bcolors.FAIL}Error during recovery: {e}{bcolors.ENDC}")
        except json.JSONDecodeError as e:
            print(f"{bcolors.WARNING}Warning: Could not parse error recovery response as JSON: {e}{bcolors.ENDC}")
            print(f"Raw response: {error_response.text}")

    async def execute_recovery_step(self, step):
        if step["type"] == "reset_state":
            self.state_of_mind = self.load_state_of_mind()
        elif step["type"] == "reload_tools":
            self.tool_manager.reload_tools()
        elif step["type"] == "reinitialize_models":
            self.initialize_models()
        # Add more recovery steps as needed

    def implement_improvement(self, improvement):
        if improvement["type"] == "add_tool":
            self.tool_manager.add_tool(improvement["tool_info"])
        elif improvement["type"] == "update_prompt":
            UpdatePrompts(improvement["prompt_key"], improvement["new_prompt"])
        elif improvement["type"] == "adjust_emotion_weights":
            self.emotions = {k: v * improvement["weight"] for k, v in self.emotions.items()}
            self.save_json(EMOTIONS_FILE, self.emotions)
        # Add more improvement types as needed

    def update_long_term_memory(self, response):
        """Updates long-term memory based on a response."""
        try:
            new_knowledge = json.loads(response.text)
            self.long_term_memory.append(new_knowledge)
            if len(self.long_term_memory) > 1000:
                self.long_term_memory.pop(0)
        except json.JSONDecodeError as e:
            self.log_json_error("learning response", e, response.text)

if __name__ == "__main__":
    ai = GeminiSelfAwareAI()
    # Start the asynchronous loop
    asyncio.run(ai.run())