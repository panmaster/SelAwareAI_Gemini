import google.generativeai as genai
import ast
from datetime import datetime
import hashlib
import os
import logging
from termcolor import colored  # Import the termcolor library
import Tool_Manager as TM

MODEL_NAME = 'gemini-1.5-flash-latest'
genai.configure(api_key='AIzaSyBeyvNc9C0roQoHcOr7WnmML2WwTOtimxkE')  # Replace with your actual API key

# ANSI color codes and emojis (unchanged)
class Colors:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

TASK_EMOJI = " "
SUBTASK_EMOJI = "   └─ "
IN_PROGRESS_EMOJI = " "
COMPLETED_EMOJI = " "
FOCUS_EMOJI = " "


class AwarenessLoop:
    def __init__(self, tool_manager):
        self.tool_manager = tool_manager
        self.counter = 0
        self.models = {}

        # Load tools once
        self.tools_by_type = {
            'focus': tool_manager.get_tools_list_json(tool_type='focus'),
            'os': tool_manager.get_tools_list_json(tool_type='os')
        }

        # Set up models and instructions
        self.instructions = {
            'Introspection': "Introspection, be concise",
            'Action Planning': "Based on the system's current state, propose actions to achieve the system's goals. Be concise",
            'Action Execution': "Execute the planned actions and report the results. You can call functions",
            'Results Evaluation': "Evaluate the results of the executed actions against the system's goals. Be concise",
            'Knowledge Integration': "Integrate new insights and learnings into the system's knowledge base"
        }

        # Create models and start chat sessions
        for stage in self.instructions:
            instruction = self.instructions[stage]
            tools = self.tools_by_type.get(stage.split()[0].lower(), 'os')  # Use appropriate tool type
            self.models[stage] = genai.GenerativeModel(
                system_instruction=instruction,
                model_name=MODEL_NAME,
                tools=ast.literal_eval(tools),
                safety_settings={"HARASSMENT": "block_none"}
            )
            self.models[stage].start_chat(history=[])  # Start chat session

        # Setup logging
        logging.basicConfig(filename='awareness_loop.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

    def run_loop(self):
        loop_data = {}
        self.counter += 1

        # Run stages sequentially
        previous_data = None
        for stage in self.instructions:
            loop_data[stage] = self.run_stage(stage, previous_data)
            previous_data = loop_data[stage]

        self.save_log(loop_data)

    def run_stage(self, stage_name, previous_data=None):
        """Runs a single stage of the awareness loop."""
        instruction = self.instructions[stage_name]
        model = self.models[stage_name]
        chat_session = model.chat

        prompt = f"{instruction}\n\nPrevious stage output: {previous_data}" if previous_data else instruction
        response = chat_session.send_message(prompt)
        logging.info(f"Stage: {stage_name}, Prompt: {prompt}")
        logging.info(f"Stage: {stage_name}, Response: {response}")

        extracted_text = self.extract_text(response)
        function_calls, results = self.interpret_and_execute_function_calls(response, self.tool_manager)

        stage_data = {
            'prompt': prompt,
            'response': extracted_text,
            'function_calls': function_calls,
            'results': results
        }
        return stage_data

    def extract_text(self, response):
        """Extracts text from a Gemini API response."""
        extracted_text = ""
        for candidate in response.candidates:
            for part in candidate.content.parts:
                if part.text:
                    extracted_text += part.text
        return extracted_text.strip()

    def interpret_and_execute_function_calls(self, response, tool_manager):
        """Identifies and parses function calls from a Gemini API response, and executes them."""
        function_calls = []
        results = {}

        print(f"\n{Colors.BLUE}--- Interpreter for function calls started ---{Colors.ENDC}")
        for candidate in response.candidates:
            for part in candidate.content.parts:
                if part.function_call:
                    function_call = part.function_call
                    function_calls.append({
                        'name': function_call.name,
                        'args': function_call.arguments
                    })

        if function_calls:
            for call in function_calls:
                function_name = call['name']
                function_args_str = call['args']

                print(f"{Colors.CYAN}Calling function: {function_name}{Colors.ENDC}")
                print(f"{Colors.CYAN}Arguments (string): {function_args_str}{Colors.ENDC}")

                try:
                    function_args = ast.literal_eval(function_args_str) if function_args_str else {}
                    print(f"{Colors.CYAN}Arguments (dict): {function_args}{Colors.ENDC}")

                    tool_function = tool_manager.get_tool_by_name(function_name)

                    if tool_function:
                        result = tool_function(**function_args)
                        results[function_name] = result
                        print(f"{Colors.GREEN}Result: {result}{Colors.ENDC}")
                    else:
                        print(f"{Colors.WARNING}Tool function '{function_name}' not found{Colors.ENDC}")

                except (SyntaxError, ValueError) as e:
                    print(f"{Colors.FAIL}Error parsing function arguments: {e}{Colors.ENDC}")

            print(f"\n{Colors.BLUE}--- Results returned from function calls ---{Colors.ENDC}")
            for func, res in results.items():
                print(f"{Colors.CYAN}{func}: {res}{Colors.ENDC}")

            print(f"\n{Colors.BLUE}Final Results:{Colors.ENDC}")

            print(f"{Colors.CYAN}Function Calls: {function_calls}{Colors.ENDC}")

            print(f"{Colors.BLUE}--- Interpreter for function calls finished ---{Colors.ENDC}\n")

        return function_calls, results

    def create_session_with_sanitisation(self):
        now = datetime.now()
        date_time_str = now.strftime("%Y-%m-%d %H:%M:%S.%f")
        date_time_bytes = date_time_str.encode('utf-8')
        hash_object = hashlib.sha256(date_time_bytes)
        return hash_object.hexdigest()

    def save_log(self, loop_data):
        session_id = self.create_session_with_sanitisation()
        filepath = f"conversationLogs/log_{session_id}"
        os.makedirs(os.path.dirname(filepath), exist_ok=True)

        print(f"{Colors.GREEN}Saving log{Colors.ENDC}")
        with open(filepath, "a+") as f:
            f.write(f"----------------------Session {session_id}---------------------------\n")
            for stage, data in loop_data.items():
                f.write(f"{stage.upper()} PROMPT:\n{data['prompt']}\n")
                f.write(f"{stage.upper()} RESPONSE:\n{data['response']}\n****\n")

# Main Code
if __name__ == "__main__":
    tool_manager = TM.ToolManager()
    awareness_loop = AwarenessLoop(tool_manager)
    awareness_loop.run_loop()