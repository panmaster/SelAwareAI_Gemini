import google.generativeai as genai
import json
from typing import List, Dict, Callable
import logging
import os
import re
from TOOL_MANAGER import ToolManager

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Replace with your actual API key
API_KEY = "AIzaSyAlyMsmyOfJiGBmvaJBwHJC7GdalLJ_e2k"
genai.configure(api_key=API_KEY)

# --- ANSI Color Codes ---
class Color:
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
    print(color + text + Color.ENDC)


# --- Tool Definitions ---
tools_folder = "tools"
tool_manager = ToolManager(tools_folder)
toolsStr = tool_manager.get_tool_descriptions()

# Format and sanitize tool descriptions for the planner
formatted_tools = ""
i = 1  # Counter for numbering the tools
for name, description in toolsStr.items():
    tool_type = tool_manager.tools[name].tool_type  # Get the tool type
    formatted_tools += f" {i}.'{name}'='{description.strip()}'\n"
    i += 1  # Increment the counter for the next tool

print()
print(formatted_tools)

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
                            if tool_name == 'retrieve_tools_by_names':
                                tool_function=tool_manager.retrieve_tools_by_names


                            function_args = {}
                            for arg_name, arg_value in function_call.args.items():
                                function_args[arg_name] = arg_value

                            print(f"Function name: {Color.OKGREEN}{function_call.name}{Color.ENDC}")
                            for key, value in function_args.items():
                                print(f"        {Color.OKCYAN}{key}{Color.ENDC}: {value}")

                            try:
                                # Execute the tool function
                                result = tool_function(**function_args)
                                results.append(result)

                            except Exception as e:
                                logger.error(f"Error calling {tool_name}: {e}")
                                results.append(f"Error calling {tool_name}: {e}")
                    else:
                            logger.warning(f"Tool function '{tool_name}' not found.")
    return results


def choose_retrieve_tools_by_names(tool_names: List[str]) -> List[Callable]:
    """
    This function is called by the planner model to choose and retrieve tools.
    It takes a list of tool names and returns the actual tool functions.

    Args:
        tool_names: A list of tool names to retrieve.

    Returns:
        A list of tool functions.
    """
    print("Choosing and retrieving tools...")
    return tool_manager.retrieve_tools_by_names(tool_names)  # Retrieve tools from ToolManager





planner_model = genai.GenerativeModel(
    model_name='gemini-1.5-flash-latest',
    safety_settings={'HARASSMENT': 'block_none'},
    system_instruction=f"""You choose tools.

                           {formatted_tools}
                          """,
    tools=[tool_manager.retrieve_tools_by_names]

)

# --- Model 2: Executor ---
executor_model = genai.GenerativeModel(
    model_name='gemini-1.5-flash-latest',
    safety_settings={'HARASSMENT': 'block_none'},
    system_instruction="""You are an AI assistant that executes instructions and uses tools. 
                          """,
)

# --- Main Loop ---
planner_chat = planner_model.start_chat(history=[])
executor_chat = executor_model.start_chat(history=[])

while True:
    print()
    user_input = input(Color.OKCYAN + "What would you like to do? " + Color.ENDC)

    # --- Planning Stage ---
    print_colored(Color.OKBLUE, "\n--- Choose Tools ---")
    prompt = user_input

    planning_response = planner_chat.send_message(prompt)
    planning_text = extract_text_from_response(planning_response)
    print(planning_response)
    retrivedFunctions = INTERPRET_function_calls(planning_response, tool_manager)
    print_colored(Color.OKGREEN, f"Planner's Response: {planning_text}")

    # --- Execution Stage ---
    print_colored(Color.OKGREEN, "\n--- Execution Stage ---")




    # Execute the plan
    execution_response = executor_chat.send_message(f"{user_input}", tools= retrivedFunctions)
    execution_text = extract_text_from_response(execution_response)
    print(execution_response)
    print_colored(Color.OKBLUE, f"Executor's Response: {execution_text}")
    RESULTS_execution_function_calls = INTERPRET_function_calls(execution_response, tool_manager)


    print_colored(
        Color.OKCYAN, f"Executor's Function Calls: {RESULTS_execution_function_calls}"
    )

