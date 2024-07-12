# main_loop.py
import google.generativeai as genai
import json
from typing import List, Dict, Any
import logging
import os
import TOOL_MANAGER

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(filename)s - %(lineno)d - %(message)s')
logger = logging.getLogger(__name__)

# Replace with your actual API key
API_KEY = "AIzaSyBqdQk7ybnS3Mvpr0IhKElcvgv57o6HYnE"
genai.configure(api_key=API_KEY)

# --- Tool Definitions ---
tools_dir = "tools"
tool_manager = TOOL_MANAGER.ToolManager(tools_dir)

# --- Model Definitions ---
# --- Model 1: Planner ---
planner_model = genai.GenerativeModel(
    model_name='gemini-1.5-flash-latest',
    safety_settings={'HARASSMENT': 'block_none'},
    system_instruction="""You are an AI assistant tasked with planning tasks. 
                          You can suggest actions and tools to gather information.
                          When suggesting a tool, use the format: `[tool_name](arg1, arg2, ...)`
                          For example: `function_read_from_file(path/to/file)`
                          """
)

# --- Model 2: Executor ---
executor_model = genai.GenerativeModel(
    model_name='gemini-1.5-flash-latest',
    safety_settings={'HARASSMENT': 'block_none'},
    system_instruction="""You are an AI assistant that executes instructions and uses tools. 
                          You will receive a plan and execute it step-by-step. 
                          If the plan includes using a tool, call the appropriate function.""",

)

# --- Helper Functions ---
def extract_text_from_response(response) -> str:
    """Extracts the text content from a model response."""
    extracted_text = ""
    for candidate in response.candidates:
        for part in candidate.content.parts:
            extracted_text += part.text
    return extracted_text.strip()

def INTERPRET_function_calls(response, function_mapping) -> List[str]:
    """Interprets function calls from a Gemini response and executes them."""
    logger.info("Interpreting function calls")
    results = []
    print("interpreter")
    if response.candidates:
        for candidate in response.candidates:
            if hasattr(candidate, 'content') and hasattr(candidate.content, 'parts'):
                for part in candidate.content.parts:
                    function_call = getattr(part, 'function_call', None)
                    if function_call:
                        print("=============================")
                        function_name = function_call.name
                        function_args = function_call.args
                        print(f"Function name: {function_name}")
                        for key, value in function_args.items():
                            print(f"{key}: {value}")
                        print("==============================")

                        function_to_call = function_mapping.get(function_name)

                        if function_to_call:
                            logger.info(f"Calling function: {function_name}({function_args})")
                            try:
                                result = function_to_call(**function_args)
                                results.append(f"Result of {function_name}({function_args}): {result}")
                            except Exception as e:
                                logger.error(f"Error calling {function_name}: {e}")
                                results.append(f"Error calling {function_name}: {e}")
                        else:
                            logger.warning(f"Tool function '{function_name}' not found.")
    return results


def load_tools_of_type(tool_types: List[str]) -> List[Tool]:
    """Loads tools based on a list of tool types."""
    if not tool_types:
        return tool_manager.get_tools()  # Load all tools if no types are specified
    tools = []
    for tool_type in tool_types:
        tools.extend(tool_manager.get_tools_by_type(tool_type))
    return tools

# --- Main Loop ---
planner_chat = planner_model.start_chat(history=[])
executor_chat = executor_model.start_chat(history=[])

while True:
    user_input = input("What would you like to do? ")

    # --- Tool Selection ---
    tool_types_input = input("What type of tools do you want to use? (Comma-separated, e.g., 'file, web', or 'all' for all): ")
    tool_types = [t.strip() for t in tool_types_input.split(",") if t.strip()]
    tools = tool_manager.get_tools(*tool_types)

    # --- Planning Stage ---
    print("\n--- Planning Stage ---")
    planning_response = planner_chat.send_message(user_input)
    planning_text = extract_text_from_response(planning_response)
    planning_function_calls = INTERPRET_function_calls(planning_response, tools)
    print(f"Planner's Response: {planning_text}")
    print(f"Planner's Function Calls: {planning_function_calls}")

    # --- Execution Stage ---
    print("\n--- Execution Stage ---")
    executor_chat = executor_model.start_chat(history=[], tools=tools)  # Update the executor with the chosen tools
    execution_response = executor_chat.send_message(f"The plan is: {planning_text}")
    execution_text = extract_text_from_response(execution_response)
    execution_function_calls = INTERPRET_function_calls(execution_response, tools)
    print(f"Executor's Response: {execution_text}")
    print(f"Executor's Function Calls: {execution_function_calls}")

# --- End ---
print("Exiting the loop.")