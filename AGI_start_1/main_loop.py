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
API_KEY = "AIzaSyBqdQk7ybnS3Mvpr0IhKElcvgv57o6HYnE"
genai.configure(api_key=API_KEY)

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
                        tool_name = function_call.name
                        tool_function = tool_manager.get_tool_function(tool_name)

                        if tool_function:
                            # Extract arguments and map them to function parameters
                            function_args = {}
                            for arg_name, arg_value in function_call.args.items():
                                function_args[arg_name] = arg_value

                            logger.info(f"Calling function: {tool_name}({function_args})")
                            try:
                                # Execute the tool function
                                result = tool_function(**function_args)
                                results.append(f"Result of {tool_name}({function_args}): {result}")
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
                          You can suggest actions and tools to gather information.""",
    tools=[tool.function for tool in tool_manager.get_all_tools()]
)

# --- Model 2: Executor ---
executor_model = genai.GenerativeModel(
    model_name='gemini-1.5-flash-latest',
    safety_settings={'HARASSMENT': 'block_none'},
    system_instruction="""You are an AI assistant that executes instructions and uses tools. 
                          You will receive a plan and execute it step-by-step. 
                          If the plan includes using a tool, call the appropriate function.""",
    tools=[tool.function for tool in tool_manager.get_all_tools()]
)

# --- Main Loop ---
planner_chat = planner_model.start_chat(history=[])
executor_chat = executor_model.start_chat(history=[])

while True:
    user_input = input("What would you like to do? ")

    # --- Planning Stage ---
    print("\n--- Planning Stage ---")
    planning_response = planner_chat.send_message(user_input)
    planning_text = extract_text_from_response(planning_response)
    planning_function_calls = INTERPRET_function_calls(planning_response, tool_manager)
    print(planning_response)
    print(f"Planner's Response: {planning_text}")
    print(f"Planner's Function Calls: {planning_function_calls}")

    # --- Execution Stage ---
    print("\n--- Execution Stage ---")
    execution_response = executor_chat.send_message(f"The plan is: {planning_text}")
    execution_text = extract_text_from_response(execution_response)
    execution_function_calls = INTERPRET_function_calls(execution_response, tool_manager)
    print(execution_response)
    print(f"Executor's Response: {execution_text}")
    print(f"Executor's Function Calls: {execution_function_calls}")

# --- End ---
print("Exiting the loop.")