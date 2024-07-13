import google.generativeai as genai
import json
from typing import List, Dict
import logging
import os
from TOOL_MANAGER import ToolManager  # Import the ToolManager class

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Replace with your actual API key
API_KEY = "AIzaSyAlyMsmyOfJiGBmvaJBwHJC7GdalLJ_e2k"
genai.configure(api_key=API_KEY)


# --- ANSI Color Codes ---
class Color:
    """
    A class to define ANSI escape codes for coloring text in the terminal.
    """
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


def print_colored(color, text):
    """
    Prints text with the specified color.

    Args:
        color (str): The color code to use.
        text (str): The text to print.
    """
    print(color + text + Color.ENDC)


# --- Tool Definitions ---
tools_folder = "tools"
tool_manager = ToolManager(tools_folder)  # Initialize ToolManager


# --- Helper Functions ---
def extract_text_from_response(response) -> str:
    """Extracts the text content from a model response."""
    extracted_text = ""
    for candidate in response.candidates:
        for part in candidate.content.parts:
            extracted_text += part.text
    return extracted_text.strip()


def INTERPRET_function_calls(response, tool_manager) -> List[str]:
    """Interprets function calls from the model response and executes them."""

    results = []
    if response.candidates:
        for candidate in response.candidates:
            if hasattr(candidate, 'content') and hasattr(candidate.content, 'parts'):
                for part in candidate.content.parts:
                    function_call = getattr(part, 'function_call', None)
                    if function_call:
                        print_colored(Color.OKBLUE, "---------------INTERPRETER-------------------")
                        tool_name = function_call.name
                        tool_function = tool_manager.get_tool_function(tool_name)

                        if tool_function:
                            # Extract arguments and map them to function parameters
                            function_args = {}
                            for arg_name, arg_value in function_call.args.items():
                                function_args[arg_name] = arg_value

                            print(f"Function name: {Color.OKGREEN}{function_call.name}{Color.ENDC}")
                            for key, value in function_args.items():
                                print(f"        {Color.OKCYAN}{key}{Color.ENDC}: {value}")

                            try:
                                # Execute the tool function
                                result = tool_function(**function_args)
                                results.append(
                                    f"Result of {Color.OKGREEN}{tool_name}{Color.ENDC}({function_args}): {result}")
                            except Exception as e:
                                logger.error(f"Error calling {tool_name}: {e}")
                                results.append(f"Error calling {tool_name}: {e}")
                        else:
                            logger.warning(f"Tool function '{tool_name}' not found.")
    return results


# --- Model Definitions ---
# --- Model 1: Planner ---
planner_model = genai.GenerativeModel(
    model_name='gemini-1.5-flash-latest',
    safety_settings={'HARASSMENT': 'block_none'},
    system_instruction="""You are an AI assistant tasked with planning tasks. 
                          You can suggest actions and tools to gather information.
                          Respond in a structured format with clear steps and tool calls, if needed.
                          For example:
                          1. Read the content of file 'data.txt' using the tool 'read_from_file'
                          2. Analyze the data
                          3. ...""",

)

# --- Model 2: Executor ---
executor_model = genai.GenerativeModel(
    model_name='gemini-1.5-flash-latest',
    safety_settings={'HARASSMENT': 'block_none'},
    system_instruction="""You are an AI assistant that executes instructions and uses tools. 
                          You will receive a plan and execute it step-by-step. 
                          If the plan includes using a tool, call the appropriate function.""",
    tools=tool_manager.load_tools_of_type("all")  # Load all tools initially
)

# --- Main Loop ---
planner_chat = planner_model.start_chat(history=[])
executor_chat = executor_model.start_chat(history=[])

while True:
    print()
    user_input = input(Color.OKCYAN + "What would you like to do? " + Color.ENDC)

    # --- Planning Stage ---
    print_colored(Color.OKBLUE, "\n--- Planning Stage ---")
    planning_response = planner_chat.send_message(user_input)
    planning_text = extract_text_from_response(planning_response)
    planning_function_calls = INTERPRET_function_calls(planning_response, tool_manager)
    print_colored(Color.OKGREEN, f"Planner's Response: {planning_text}")
    print_colored(Color.OKCYAN, f"Planner's Function Calls: {planning_function_calls}")

    # --- Execution Stage ---
    print_colored(Color.OKGREEN, "\n--- Execution Stage ---")

    # Determine which tools to load based on the plan
    tools_to_load = []
    for line in planning_text.split('\n'):
        if "using the tool" in line:
            tool_name = line.split("'")[1]  # Extract the tool name
            tools_to_load.append(tool_name)

    # Load only the required tools (if not already loaded)
    for tool_name in tools_to_load:
        if tool_name not in [tool.function.__name__ for tool in executor_model.tools]:
            tool_function = tool_manager.get_tool_function(tool_name)
            if tool_function:
                executor_model.add_tool(tool_function)
                logger.info(f"Added tool {tool_name} for execution.")
            else:
                logger.warning(f"Tool {tool_name} not found. Skipping.")

    execution_response = executor_chat.send_message(f"The plan is: {planning_text}")
    execution_text = extract_text_from_response(execution_response)
    execution_function_calls = INTERPRET_function_calls(execution_response, tool_manager)
    print_colored(Color.OKBLUE, f"Executor's Response: {execution_text}")
    print_colored(Color.OKCYAN, f"Executor's Function Calls: {execution_function_calls}")

    # Remove loaded tools for the next iteration
    for tool_name in tools_to_load:
        tool_function = tool_manager.get_tool_function(tool_name)
        if tool_function:  # Only remove if the tool was successfully loaded
            executor_model.remove_tool(tool_function)
            logger.info(f"Removed tool {tool_name} for the next iteration.")

# --- End ---
print_colored(Color.OKGREEN, "Exiting the loop. 👋")