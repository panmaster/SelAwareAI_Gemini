import os
import google.generativeai as genai
import json
from typing import List, Dict, Callable, Tuple
import logging
from TOOL_MANAGER import ToolManager
import time


def create_embeded_modelium_function(model_configs, max_loops=None, output_filename="generated_modelium.py"):
    """
    Generates Python code for a Modelium function with looping, feedback mechanisms,
    and proper handling of tool access and results.

    Args:
        model_configs (list): List of dictionaries, each with keys:
                                - 'model_name': Name for the model variable.
                                - 'model_type': PaLM 2 model type.
                                - 'system_instruction': Model's instructions.
                                - 'prompt': Prompt template. Can use placeholders:
                                    - {{user_input}}
                                    - {{previous_responses}} (a list containing outputs of previous models)
                                - 'tool_access': 'none', 'chooser', or 'all'.
        max_loops (int): Maximum number of loops to run. If None, runs indefinitely.
        output_filename (str): Output Python filename.
    """

    # --- Code Template ---
    code_template = """
import google.generativeai as genai
import json
from typing import List, Dict, Callable, Tuple
import logging
import os
import re
from TOOL_MANAGER import ToolManager
import time

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Replace with your actual API key
API_KEY = "YOUR_API_KEY" 
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
i = 1  
for name, description in toolsStr.items():
    tool_type = tool_manager.tools[name].tool_type 
    formatted_tools += f" {{i}}. '{{{{name}}}}' = '{{{{description.strip()}}}}' "
    i += 1 

# --- Helper Functions ---
def extract_text_from_response(response) -> str:
    extracted_text = ""
    for candidate in response.candidates:
        for part in candidate.content.parts:
            extracted_text += part.text
    return extracted_text.strip()

def INTERPRET_function_calls(response, tool_manager) -> List[str]:
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

                        function_args = {{}}
                        for arg_name, arg_value in function_call.args.items():
                            function_args[arg_name] = arg_value

                        print(f"Function name: {{Color.OKGREEN}}{{function_call.name}}{{Color.ENDC}}")
                        for key, value in function_args.items():
                            print(f"        {{Color.OKCYAN}}{{key}}{{Color.ENDC}}: {{value}}")

                        try:
                            result = tool_function(**function_args)
                            results.append(result)

                        except Exception as e:
                            logger.error(f"Error calling {{tool_name}}: {{e}}")
                            results.append(f"Error calling {{tool_name}}: {{e}}")
                    else:
                        logger.warning(f"Tool function '{{tool_name}}' not found.")
    return results

def choose_retrieve_tools_by_names(tool_names: List[str]) -> List[Callable]:
    print("Choosing and retrieving tools...")
    return tool_manager.retrieve_tools_by_names(tool_names) 

# --- Model Initialization ---
{model_init_code}

def run_modelium(user_input: str, max_loops: int = None) -> Tuple[bool, Dict[str, List[str]]]:
    previous_responses = []
    all_responses = {{}}
    loop_count = 0

    while True:
        if max_loops is not None and loop_count >= max_loops:
            return True, all_responses  # Success, but reached max loops

        loop_count += 1

        try:
            # --- Model Interaction ---
{model_interaction_code}

            # Check for completion condition (you may want to customize this)
            if "TASK_COMPLETE" in extract_text_from_response(response_{num_models}):
                return True, all_responses  # Success

        except Exception as e:
            logger.error(f"Error in modelium execution: {{e}}")
            return False, {{"error": str(e)}}  # Failure

        # Optional: Add logic to break the loop based on other conditions
        # For example:
        # if some_condition_is_met:
        #     return True, all_responses

    return True, all_responses  # This line should not be reached, but it's here for completeness

# Example usage
if __name__ == "__main__":
    user_input = input("What would you like to do? ")
    success, results = run_modelium(user_input, max_loops=5)

    if success:
        print("Modelium execution successful:")
        for model, responses in results.items():
            print(f"{{model}}:")
            for response in responses:
                print(f"  - {{response}}")
    else:
        print("Modelium execution failed:", results["error"])
"""

    # --- Generate Model Initialization Code ---
    model_init_code = ""
    for model_config in model_configs:
        model_name = model_config['model_name']
        model_type = model_config['model_type']
        tool_access = model_config['tool_access']
        system_instruction = model_config['system_instruction']

        if tool_access == 'chooser':
            # Append tool information to the system instruction:
            system_instruction += '''
                              You are a helpful and polite AI assistant that will plan and choose the right tools to complete the task.
                              You have the following tools available:
                               {formatted_tools}
                              '''

        model_init_code += f"{model_name} = genai.GenerativeModel(\n"
        model_init_code += f"    model_name='{model_type}',\n"
        model_init_code += f"    system_instruction=f\"\"\"{system_instruction}\"\"\",\n"

        if tool_access == 'chooser':
            model_init_code += f"    tools=[tool_manager.retrieve_tools_by_names],\n"
        elif tool_access == 'all':
            model_init_code += f"    tools=tool_manager.get_all_tool_functions(), \n"

        model_init_code += ")\n"
        model_init_code += f"{model_name}_chat = {model_name}.start_chat(history=[])\n\n"

    # --- Generate Model Interaction Code ---
    model_interaction_code = ""
    num_models = len(model_configs)
    for i, model_config in enumerate(model_configs):
        model_name = model_config['model_name']
        prompt = model_config['prompt']
        tool_access = model_config['tool_access']

        model_interaction_code += f"            # --- {model_name} Interaction ---\n"
        model_interaction_code += f"            response_{i + 1} = {model_name}_chat.send_message(f'''{prompt}'''.format(user_input=user_input, previous_responses=previous_responses))\n"
        model_interaction_code += f"            print(response_{i + 1})\n"
        model_interaction_code += f"            retrieved_functions_results = INTERPRET_function_calls(response_{i + 1}, tool_manager)\n"
        model_interaction_code += f"            response_text = extract_text_from_response(response_{i + 1})\n"
        model_interaction_code += f"            print_colored(Color.OKGREEN, f\"{model_name} Response: {{response_text}}\")\n"
        model_interaction_code += f"            all_responses.setdefault('{model_name}', []).append(response_text)\n"
        model_interaction_code += f"            previous_responses.append(response_text)\n"
        if tool_access == 'all':
            model_interaction_code += f"            previous_responses.extend(retrieved_functions_results)\n"
            model_interaction_code += f"            all_responses.setdefault('{model_name}_tools', []).extend(retrieved_functions_results)\n"
        model_interaction_code += "\n"

    # --- Create the Final Code ---
    final_code = code_template.format(
        model_init_code=model_init_code,
        model_interaction_code=model_interaction_code,
        num_models=num_models
    )

    # --- Write to File ---
    with open(output_filename, "w") as f:
        f.write(final_code)

    print(f"Modelium function code has been generated and saved to {output_filename}")


# Example usage
model_configs = [
    {
        'model_name': 'initiator',
        'model_type': 'gemini-1.5-flash-latest',
        'system_instruction': "You are a helpful AI assistant. Engage in a conversation with the user and gather their requirements.",
        'prompt': "User input: {{user_input}}",
        'tool_access': 'none'
    },
    {
        'model_name': 'planner',
        'model_type': 'gemini-1.5-flash-latest',
        'system_instruction': "You are a helpful AI assistant that plans how to answer user questions using tools.",
        'prompt': "The user asked: {{previous_responses}}. Create a plan using available tools.",
        'tool_access': 'chooser'
    },
    {
        'model_name': 'executor',
        'model_type': 'gemini-1.5-flash-latest',
        'system_instruction': "You are a helpful AI assistant that executes tasks using provided tools.",
        'prompt': "Execute the following plan: {{previous_responses}} and provide the result to answer the user's question.",
        'tool_access': 'all'
    },
    {
        'model_name': 'summarizer',
        'model_type': 'gemini-1.5-flash-latest',
        'system_instruction': "You are a helpful AI assistant that summarizes information.",
        'prompt': "Summarize the following information: {{previous_responses}}. If the task is complete, include 'TASK_COMPLETE' in your response.",
        'tool_access': 'none'
    }
]

# Call the function to create the Modelium code
create_embeded_modelium_function(model_configs, max_loops=5, output_filename="my_4_model_modelium_function.py")