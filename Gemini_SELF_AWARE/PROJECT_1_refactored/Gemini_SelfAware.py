# -*- coding: utf-8 -*-
import os
import datetime
from abc import ABC, abstractmethod
from typing import List, Dict, Any

import google.generativeai as genai

# --- Import your custom modules ---
from Tool_Manager import ToolManager
from MEMORY______________frame_creation import CREATE_MEMORY_FRAME____
from SomeMemoryScript______MemoryRetrival import RETRIVE_RELEVANT_FRAMES

RETRIVE_RELEVANT_FRAMES_json_description = {
    "function_declarations": [
        {
            "name": "RETRIVE_RELEVANT_FRAMES",
            "description": "Retrieves relevant frames from memory based on a query using cosine similarity and returns the top 5 frames with their similarity scores.",
            "parameters": {
                "type_": "OBJECT",
                "properties": {
                    "query": {
                        "type_": "STRING",
                        "description": "The query to search for relevant frames."
                    }
                },
                "required": ["query"]
            },
            "return_type": "STRING",
            "return_description": "A string containing the top 5 relevant frames, each with its similarity score, in JSON format."
        }
    ]
}

# --- Configuration ---
genai.configure(api_key='YOUR_API_KEY_HERE')  # Replace with your API key

SESSION_FOLDER = "sessions"
MEMORY_FOLDER = "memories"
MEMORY_STRUCTURE_SUMMARY_FILE = "memory_structure_summary.txt"

# --- Color Codes for Terminal Output ---
COLORS = {
    "reset": "\033[0m",
    "yellow": "\033[33m",
    "cyan": "\033[36m",
    "green": "\033[32m",
    "magenta": "\033[35m",
    "blue": "\033[94m",
    "red": "\033[31m",  # Add red for errors
    "bold": "\033[1m", # Add bold for emphasis
}


# --- Function Interpreter Base Class ---
class FunctionInterpreter(ABC):
    """Abstract base class for function interpreters."""

    @abstractmethod
    def interpret(self, function_call, **kwargs) -> str:
        """Interprets a function call and returns the result.

        Args:
            function_call: The function call object.
            **kwargs: Additional keyword arguments.

        Returns:
            The result of the function call.
        """
        pass


# --- Tool Function Interpreter ---
class ToolFunctionInterpreter(FunctionInterpreter):
    """Interprets function calls for tools."""

    def __init__(self, tool_manager: ToolManager):
        self.tool_manager = tool_manager

    def interpret(self, function_call, **kwargs) -> str:
        """Interprets tool function calls."""
        function_name = function_call.name
        function_arguments = function_call.args
        function_to_call = self.tool_manager.tool_mapping.get(function_name)

        if function_to_call:
            print(f"{COLORS['blue']}FUNCTION CALL:{COLORS['reset']} {function_name}({function_arguments}) ")
            try:
                results = function_to_call(**function_arguments)
                return f"{COLORS['green']}Result of {function_name}({function_arguments}):{COLORS['reset']} {results}"
            except Exception as e:
                return f"{COLORS['red']}Error during tool execution: {e}{COLORS['reset']}"
        else:
            return f"{COLORS['red']}Warning: Function '{function_name}' not found.{COLORS['reset']}"


# --- Memory Function Interpreter ---
class MemoryFunctionInterpreter(FunctionInterpreter):
    """Interprets function calls for memory retrieval."""

    def interpret(self, function_call, **kwargs) -> str:
        """Interprets memory function calls."""
        function_name = function_call.name
        function_arguments = function_call.args

        if function_name == "RETRIVE_RELEVANT_FRAMES":
            print(
                f"{COLORS['magenta']}MEMORY RETRIEVAL:{COLORS['reset']} retrieve_relevant_frames(query='{function_arguments.get('query')}')"
            )
            try:
                results = RETRIVE_RELEVANT_FRAMES(**function_arguments)
                return f"{COLORS['green']}Result of {function_name}({function_arguments}):{COLORS['reset']} {results}"
            except Exception as e:
                return f"{COLORS['red']}Error during memory retrieval: {e}{COLORS['reset']}"
        else:
            return f"{COLORS['red']}Warning: Memory function '{function_name}' not found.{COLORS['reset']}"


# --- Function Call Handler ---
class FunctionCallHandler:
    """Handles the interpretation and execution of function calls."""

    def __init__(self):
        self.interpreters = {}

    def register_interpreter(
        self, function_name: str, interpreter: FunctionInterpreter
    ):
        """Registers a function interpreter for a specific function."""
        self.interpreters[function_name] = interpreter

    def handle_function_call(self, function_call, **kwargs) -> str:
        """Handles a function call by finding the appropriate interpreter."""
        function_name = function_call.name
        interpreter = self.interpreters.get(function_name)

        if interpreter:
            return interpreter.interpret(function_call, **kwargs)
        else:
            return f"{COLORS['red']}Warning: No interpreter found for function '{function_name}'.{COLORS['reset']}"


# --- Helper Functions ---
def sanitize_time_string(time_str: str) -> str:
    """Sanitizes a time string for file naming."""
    return "".join(char for char in time_str if char.isalnum() or char in ("_", "-"))


def create_session_folder() -> str:
    """Creates a new session folder and returns its path."""
    session_timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    session_name = f"session_{session_timestamp}"
    session_path = os.path.join(SESSION_FOLDER, session_name)
    os.makedirs(session_path, exist_ok=True)
    return session_path


def summarize_memory_folder_structure(
    output_file: str = MEMORY_STRUCTURE_SUMMARY_FILE,
) -> str:
    """Summarizes the memory folder structure and writes it to a file."""
    memory_path = MEMORY_FOLDER
    summary = ""
    for root, dirs, files in os.walk(memory_path):
        relative_path = os.path.relpath(root, memory_path)
        summary += f"{relative_path}\n"
        for dir in sorted(dirs):
            summary += f"  - {dir}\n"
        for file in sorted(files):
            summary += f"    - {file}\n"

    with open(output_file, "w", encoding="utf-8") as f:
        f.write(summary)
    return summary


def gather_introspection_data(
    user_input: str, memory_summary: str, previous_loop_results: str
) -> List[str]:
    """Gathers information and context for introspection."""
    current_time = datetime.datetime.now().strftime("%H:%M:%S")
    return [
        f"{current_time} {COLORS['bold']}User Input:{COLORS['reset']} {user_input}",
        f"{COLORS['bold']}Current Memory Structure:{COLORS['reset']}\n{memory_summary}",
        f"{COLORS['bold']}Results from Previous Loop:{COLORS['reset']}\n{previous_loop_results}",
        "What are my available tools and resources?",
        "Current sensory input (Image, Audio, Text): None, None, None",
        "What are my short-term goals?",
        "What are my long-term goals?",
        "What do I want?",
        "What do I feel?",
        "What do I need?",
        "What am I experiencing?",
    ]


def perform_reflection(introspection_results: str) -> str:
    """Constructs and sends the reflection prompt to the model."""
    reflection_prompt = f"""
        {COLORS['bold']}Based on the following introspection:{COLORS['reset']}
        {introspection_results}

        {COLORS['bold']}Answer these questions:{COLORS['reset']}
        1. What is my current focus?
        2. Should I set a new goal? If so, what is it? If not, why not?
        3. Are there any problems, unknowns, or paradoxes in my memory?
        4. What problems need to be solved?
        5. What are possible courses of action based on available information?
        6. Should I:
           a) Think step-by-step?
           b) Focus on a specific aspect?
           c) Defocus and broaden my attention?
        7. Should I be more verbose in my responses? (Yes/No)
        8. Should I be less verbose? (Yes/No)
        9. Should I change the subject or keep discussing this? (Yes/No)
        10. Should I summarize the current discussion? (Yes/No)
        11. Should I dive deeper into a specific topic? (Yes/No)
        12. Should I store any of this information in my long-term memory? 
        13. Should I query my memory for relevant information?
        14. What is the status of my current goals? 
    """
    return reflection_prompt


def plan_actions(reflection_results: str) -> str:
    """Constructs and sends the action planning prompt to the model."""
    current_time = datetime.datetime.now().strftime("%H:%M:%S")
    action_prompt = (
        f"{current_time} - {COLORS['bold']}Based on this reflection:{COLORS['reset']}\n{reflection_results}\nPlan my next actions."
    )
    return action_prompt


def execute_functions(
    action_response, function_call_handler: FunctionCallHandler
) -> str:
    """Executes functions called by the model."""
    function_call_results = ""
    if action_response.candidates:
        for part in action_response.candidates[0].content.parts:
            if hasattr(part, "function_call"):
                function_call_result = function_call_handler.handle_function_call(
                    part.function_call
                )
                print(
                    f"{COLORS['magenta']}Function Call Results:\n{function_call_result}{COLORS['reset']}"
                )
                function_call_results += f"{function_call_result}\n"
    return function_call_results


def store_conversation_frame(
    introspection_results: str,
    reflection_results: str,
    action_plan: str,
    function_call_results: str,
):
    """Stores the conversation frame in memory."""
    current_conversation_frame = (
        f"Introspection:\n{introspection_results}\n"
        f"Reflection:\n{reflection_results}\n"
        f"Action Plan:\n{action_plan}\n"
        f"Function Call Results:\n{function_call_results}\n"
    )
    CREATE_MEMORY_FRAME____(current_conversation_frame)


def log_conversation(
    conversation_log_path: str, iteration_count: int, current_conversation_frame: str
):
    """Logs the conversation to a file."""
    current_time = datetime.datetime.now().strftime("%H:%M:%S")
    with open(conversation_log_path, "a+", encoding="utf-8") as log_file:
        log_file.write(f"--- Awareness Loop: {iteration_count} ---\n")
        log_file.write(f"Time: {current_time}\n")
        log_file.write(current_conversation_frame)
        log_file.write("-" * 20 + "\n\n")


def main():
    tool_manager = ToolManager()
    function_call_handler = FunctionCallHandler()
    function_call_handler.register_interpreter(
        "RETRIVE_RELEVANT_FRAMES", MemoryFunctionInterpreter()
    )
    # Add other interpreters as needed
    for tool in tool_manager.get_tools_list_json():
        function_call_handler.register_interpreter(
            tool["function_declarations"][0]["name"],
            ToolFunctionInterpreter(tool_manager),
        )

    print(f"\n{COLORS['blue']}Loaded Tool Descriptions:{COLORS['reset']}\n")
    for i, tool_json in enumerate(tool_manager.get_tools_list_json()):
        print(f"{COLORS['blue']}{i + 1}. {COLORS['reset']}{tool_json}")

    # --- Separate Models for Each Stage ---
    introspection_model = genai.GenerativeModel(
        system_instruction="""You are responsible for introspection. Analyze the current state 
                             of the system and its environment. """,
        model_name="gemini-1.5-flash-latest",
        safety_settings={"HARASSMENT": "block_none"},
    )

    reflection_model = genai.GenerativeModel(
        system_instruction="""You are responsible for reflection. Analyze the results of 
                             introspection and identify goals, problems, and potential courses 
                             of action. """,
        model_name="gemini-1.5-flash-latest",
        safety_settings={"HARASSMENT": "block_none"},
    )

    # --- Ensure tools is a flat list ---
    available_tools = tool_manager.get_tools_list_json()
    available_tools.append(RETRIVE_RELEVANT_FRAMES_json_description)

    action_model = genai.GenerativeModel(
        system_instruction="""You are responsible for action planning. Choose specific actions 
                             based on reflection and available tools. Use the "Call tool:" format. """,
        model_name="gemini-1.5-flash-latest",
        safety_settings={"HARASSMENT": "block_none"},
        tools=available_tools,
    )

    # --- Start Separate Chat Sessions ---
    introspection_chat = introspection_model.start_chat(history=[])
    reflection_chat = reflection_model.start_chat(history=[])
    action_chat = action_model.start_chat(history=[])

    session_path = create_session_folder()
    conversation_log_path = os.path.join(session_path, "conversation_log.txt")

    iteration_count = 0
    user_input_count = 0
    function_call_results = ""
    current_conversation_frame = ""

    while True:
        try:
            # User Input
            if iteration_count % 4 == 0:
                user_input = input(
                    f"{COLORS['cyan']}Enter your input (or press Enter to skip):{COLORS['reset']} "
                )
                user_input_count += 1
            else:
                user_input = ""

            # --- Awareness Loop ---
            print(
                f"{COLORS['bold']}{COLORS['green']}**************** Awareness Loop ****************{COLORS['reset']}"
            )
            print(
                f"{COLORS['green']}Awareness Loop: {iteration_count}{COLORS['reset']}"
            )
            iteration_count += 1

            memory_summary = summarize_memory_folder_structure()

            # --- Introspection ---
            print(f"{COLORS['yellow']}Introspection:{COLORS['reset']}")
            introspection_data = gather_introspection_data(
                user_input, memory_summary, function_call_results
            )
            introspection_response = introspection_chat.send_message(
                introspection_data
            )
            print(
                f"{COLORS['yellow']}{introspection_response.text}{COLORS['reset']}\n"
            )

            # --- Reflection ---
            print(f"{COLORS['cyan']}Reflection:{COLORS['reset']}")
            reflection_prompt = perform_reflection(introspection_response.text)
            reflection_response = reflection_chat.send_message(reflection_prompt)
            print(f"{COLORS['cyan']}{reflection_response.text}{COLORS['reset']}\n")

            # --- Action Planning ---
            print(f"{COLORS['green']}Action Planning:{COLORS['reset']}")
            action_prompt = plan_actions(reflection_response.text)
            action_response = action_chat.send_message(action_prompt)
            print(f"{COLORS['green']}{action_response.text}{COLORS['reset']}\n")

            # --- Function Execution ---
            print(f"{COLORS['magenta']}Function Execution:{COLORS['reset']}")
            function_call_results = execute_functions(
                action_response, function_call_handler
            )

            # --- Store Conversation Frame ---
            store_conversation_frame(
                introspection_response.text,
                reflection_response.text,
                action_response.text,
                function_call_results,
            )

            # --- Log Conversation ---
            log_conversation(
                conversation_log_path, iteration_count, current_conversation_frame
            )

            print(
                f"{COLORS['bold']}{COLORS['green']}*************************************************{COLORS['reset']}\n"
            )

        except Exception as e:
            print(f"{COLORS['red']}Error: {e}{COLORS['reset']}")
            break


if __name__ == "__main__":
    main()