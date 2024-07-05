import google.generativeai as genai
import ast
from datetime import datetime
import hashlib
import os
from termcolor import colored  # Import the termcolor library
import Tool_Manager as TM

MODEL_NAME = 'gemini-1.5-flash-latest'
genai.configure(api_key='AIzaSyDRG9wrwwpO5fCo8ALChdkTN4rOrueNbOE')  # Replace with your actual API key

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

        # Introspection Stage
        self.introspection_instruction = "Introspection, be concise"
        self.introspection_tools = self.tool_manager.get_tools_list_json(tool_type='focus')
        self.introspection_tools_load = ast.literal_eval(self.introspection_tools)
        self.introspection_model = genai.GenerativeModel(
            system_instruction=self.introspection_instruction,
            model_name=MODEL_NAME,
            tools=self.introspection_tools_load,
            safety_settings={"HARASSMENT": "block_none"}
        )
        # Start the chat session
        self.introspection_chat = self.introspection_model.start_chat(history=[])

        # Action Planning Stage
        self.action_planning_instruction = "Based on the system's current state, propose actions to achieve the system's goals. Be concise"
        self.action_planning_tools = self.tool_manager.get_tools_list_json(tool_type='os')
        self.action_planning_tools_load = ast.literal_eval(self.action_planning_tools)
        self.action_planning_model = genai.GenerativeModel(
            system_instruction=self.action_planning_instruction,
            model_name=MODEL_NAME,
            tools=self.action_planning_tools_load,
            safety_settings={"HARASSMENT": "block_none"}
        )
        # Start the chat session
        self.action_planning_chat = self.action_planning_model.start_chat(history=[])

        # Action Execution Stage
        self.action_execution_instruction = "Execute the planned actions and report the results. You can call functions"
        self.action_execution_tools = self.tool_manager.get_tools_list_json(tool_type='os')
        self.action_execution_tools_load = ast.literal_eval(self.action_execution_tools)
        self.action_execution_model = genai.GenerativeModel(
            system_instruction=self.action_execution_instruction,
            model_name=MODEL_NAME,
            tools=self.action_execution_tools_load,
            safety_settings={"HARASSMENT": "block_none"}
        )
        # Start the chat session
        self.action_execution_chat = self.action_execution_model.start_chat(history=[])

        # Results Evaluation Stage
        self.results_evaluation_instruction = "Evaluate the results of the executed actions against the system's goals. Be concise"
        self.results_evaluation_tools = self.tool_manager.get_tools_list_json(tool_type='os')
        self.results_evaluation_tools_load = ast.literal_eval(self.results_evaluation_tools)
        self.results_evaluation_model = genai.GenerativeModel(
            system_instruction=self.results_evaluation_instruction,
            model_name=MODEL_NAME,
            tools=self.results_evaluation_tools_load,
            safety_settings={"HARASSMENT": "block_none"}
        )
        # Start the chat session
        self.results_evaluation_chat = self.results_evaluation_model.start_chat(history=[])

        # Knowledge Integration Stage
        self.knowledge_integration_instruction = "Integrate new insights and learnings into the system's knowledge base"
        self.knowledge_integration_tools = self.tool_manager.get_tools_list_json(tool_type='os')
        self.knowledge_integration_tools_load = ast.literal_eval(self.knowledge_integration_tools)
        self.knowledge_integration_model = genai.GenerativeModel(
            system_instruction=self.knowledge_integration_instruction,
            model_name=MODEL_NAME,
            tools=self.knowledge_integration_tools_load,
            safety_settings={"HARASSMENT": "block_none"}
        )
        # Start the chat session
        self.knowledge_integration_chat = self.knowledge_integration_model.start_chat(history=[])

    def run_loop(self):
        loop_data = {}
        self.counter += 1

        # Introspection Stage
        loop_data["Introspection"] = self._run_stage("Introspection",
                                                     self.introspection_chat,  # Use the chat session
                                                     self.introspection_instruction)

        # Action Planning Stage
        loop_data["Action Planning"] = self._run_stage("Action Planning",
                                                       self.action_planning_chat,  # Use the chat session
                                                       self.action_planning_instruction,
                                                       loop_data["Introspection"])

        # Action Execution Stage
        loop_data["Action Execution"] = self._run_stage("Action Execution",
                                                        self.action_execution_chat,  # Use the chat session
                                                        self.action_execution_instruction,
                                                        loop_data["Action Planning"])

        # Results Evaluation Stage
        loop_data["Results Evaluation"] = self._run_stage("Results Evaluation",
                                                          self.results_evaluation_chat,  # Use the chat session
                                                          self.results_evaluation_instruction,
                                                          loop_data["Action Execution"])

        # Knowledge Integration Stage
        loop_data["Knowledge Integration"] = self._run_stage("Knowledge Integration",
                                                             self.knowledge_integration_chat,  # Use the chat session
                                                             self.knowledge_integration_instruction,
                                                             loop_data["Results Evaluation"])

        self.save_log(loop_data)

    def _run_stage(self, stage_name, chat_session, instruction, previous_data=None):
        """Runs a single stage of the awareness loop."""
        stage_data = {}
        prompt = f"{instruction}\n\nPrevious stage output: {previous_data}" if previous_data else instruction
        response = chat_session.send_message(prompt)  # Use send_message
        extracted_text, function_calls = self.extract_text_and_function_call(response)

        results = {}
        if function_calls:
            print(f"\n{Colors.BLUE}--- Interpreter for function calls started ---{Colors.ENDC}")
            for call in function_calls:
                function_name = call['name']
                function_args_str = call['args']

                print(f"{Colors.CYAN}Calling function: {function_name}{Colors.ENDC}")
                print(f"{Colors.CYAN}Arguments (string): {function_args_str}{Colors.ENDC}")

                try:
                    function_args = ast.literal_eval(function_args_str) if function_args_str else {}
                    print(f"{Colors.CYAN}Arguments (dict): {function_args}{Colors.ENDC}")

                    tool_function = self.tool_manager.get_tool_by_name(function_name)

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
            print(f"{Colors.CYAN}Extracted Text: {extracted_text}{Colors.ENDC}")
            print(f"{Colors.CYAN}Function Calls: {function_calls}{Colors.ENDC}")

            print(f"{Colors.BLUE}--- Interpreter for function calls finished ---{Colors.ENDC}\n")

        stage_data["prompt"] = prompt
        stage_data["response"] = extracted_text
        stage_data["function_calls"] = function_calls
        stage_data["results"] = results

        return stage_data

    def extract_text_and_function_call(self, response):
        extracted_text = ""
        function_calls = []

        for candidate in response.candidates:
            for part in candidate.content.parts:
                if part.text:
                    extracted_text += part.text
                if part.function_call:
                    function_call = part.function_call
                    function_calls.append({
                        'name': function_call.name,
                        'args': function_call.arguments
                    })

        return extracted_text, function_calls

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