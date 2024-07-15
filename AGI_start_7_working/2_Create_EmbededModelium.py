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
                                - 'can_write_flags': True or False.
        max_loops (int): Maximum number of loops to run. If None, runs indefinitely.
        output_filename (str): Output Python filename.
    """

    # --- Code Template ---
    code_template = """
import google.generativeai as genai
import json
from typing import List, Dict, Callable, Tuple, Any
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
    HEADER = '\\033[95m'
    OKBLUE = '\\033[94m'
    OKCYAN = '\\033[96m'
    OKGREEN = '\\033[92m'
    WARNING = '\\033[93m'
    FAIL = '\\033[91m'
    ENDC = '\\033[0m'
    BOLD = '\\033[1m'
    UNDERLINE = '\\033[4m'

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
                            tool_function = tool_manager.retrieve_tools_by_names

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

def check_stop_flags(response_text: str) -> Tuple[bool, str, str]:
    stop_flags = {{
        "**// STOP_FLAG_SUCCESS //**" : "success",
        "**// STOP_FLAG_FRUSTRATION_HIGH //**" : "frustration",
        "**// STOP_FLAG_NO_PROGRESS //**" : "no_progress",
        "**// STOP_IMMEDIATE //**" : "immediate"
    }}

    for flag, reason in stop_flags.items():
        if flag in response_text:
            return True, reason, flag
    return False, "", ""

# --- Model Initialization ---
{model_init_code}

def run_modelium(user_input: str, max_loops: int = None, break_behavior: str = "complete_loop", return_behavior: str = "all_loops") -> Tuple[bool, Dict[str, Any]]:
    previous_responses = []
    all_responses = {{}}
    loop_count = 0
    stop_flag_detected = False
    stop_reason = ""
    stop_flag = ""

    while True:
        if max_loops is not None and loop_count >= max_loops:
            return True, {{"reason": "max_loops_reached", "data": all_responses}}

        loop_count += 1

        try:
            for i, model_config in enumerate(model_configs):
                model_name = model_config['model_name']
                prompt = model_config['prompt']
                tool_access = model_config['tool_access']
                can_write_flags = model_config.get('can_write_flags', False)

                # --- Model Interaction ---
                response = globals()[f"{{model_name}}_chat"].send_message(f'''{{prompt}}'''.format(user_input=user_input, previous_responses=previous_responses))
                print(response)
                retrieved_functions_results = INTERPRET_function_calls(response, tool_manager)
                response_text = extract_text_from_response(response)
                print_colored(Color.OKGREEN, f"{{model_name}} Response: {{response_text}}")
                all_responses.setdefault(model_name, []).append(response_text)
                previous_responses.append(response_text)

                if can_write_flags:
                    should_stop, stop_reason, stop_flag = check_stop_flags(response_text)
                    if should_stop:
                        stop_flag_detected = True
                        if break_behavior == "immediate":
                            break

                if tool_access == 'all':
                    previous_responses.extend(retrieved_functions_results)
                    all_responses.setdefault(model_name + '_tools', []).extend(retrieved_functions_results)

            if stop_flag_detected and break_behavior == "complete_loop":
                break

        except Exception as e:
            logger.error(f"Error in modelium execution: {{e}}")
            return False, {{"reason": "error", "data": str(e)}}

    # Determine what to return based on return_behavior and stop_reason
    if return_behavior == "all_loops":
        return_data = all_responses
    elif return_behavior == "current_loop":
        return_data = {{model: responses[-1] for model, responses in all_responses.items()}}
    elif return_behavior == "last_response":
        last_model = list(all_responses.keys())[-1]
        return_data = all_responses[last_model][-1]
    else:
        return_data = all_responses  # Default to all_loops

    if stop_reason == "immediate":
        return True, {{
            "reason": "immediate_stop",
            "data": return_data,
            "stop_flag": stop_flag
        }}
    elif stop_reason == "success":
        return True, {{
            "reason": "success",
            "data": return_data,
            "stop_flag": stop_flag
        }}
    elif stop_reason in ["frustration", "no_progress"]:
        return False, {{
            "reason": stop_reason,
            "data": return_data,
            "stop_flag": stop_flag
        }}
    else:
        return True, {{
            "reason": "completed",
            "data": return_data
        }}

# Example usage
if __name__ == "__main__":
    user_input = input("What would you like to do? ")
    success, result = run_modelium(user_input, max_loops=5)

    if success:
        print(f"Modelium completed successfully. Reason: {{result['reason']}}")
        # Process result['data'] as needed
    else:
        print(f"Modelium encountered an issue. Reason: {{result['reason']}}")
        # Handle the failure case, possibly using result['data']
"""

    # --- Generate Model Initialization Code ---
    model_init_code = ""
    for model_config in model_configs:
        model_name = model_config['model_name']
        model_type = model_config['model_type']
        tool_access = model_config['tool_access']
        system_instruction = model_config['system_instruction']
        can_write_flags = model_config.get('can_write_flags', False)

        if can_write_flags:
            flag_instruction = """
            You can control the loop execution by including these flags in your response:
            **// STOP_FLAG_SUCCESS //** : Use when the task is successfully completed.
            **// STOP_FLAG_FRUSTRATION_HIGH //** : Use if you detect high user frustration.
            **// STOP_FLAG_NO_PROGRESS //** : Use if you detect no progress is being made.
            **// STOP_IMMEDIATE //** : Use for immediate termination of the process.
            """
            system_instruction += flag_instruction

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

    # --- Create the Final Code ---
    final_code = code_template.format(model_init_code=model_init_code)

    # --- Write to File ---
    with open(output_filename, "w") as f:
        f.write(final_code)

    print(f"Modelium function code has been generated and saved to {output_filename}")







# Example usage with 6 models
model_configs = [
    {
        'model_name': 'initiator',
        'model_type': 'gemini-1.5-flash-latest',
        'system_instruction': "You are an AI assistant that initiates conversations and gathers initial requirements from users. Be friendly and ask clarifying questions if needed.",
        'prompt': "User input: {{user_input}}\nInitiate the conversation and gather initial requirements. Ask for clarification if needed.",
        'tool_access': 'none',
        'can_write_flags': False
    },
    {
        'model_name': 'analyzer',
        'model_type': 'gemini-1.5-flash-latest',
        'system_instruction': "You are an AI assistant that analyzes user requirements and breaks them down into actionable steps.",
        'prompt': "Analyze the following user requirements and break them down into actionable steps: {{previous_responses}}",
        'tool_access': 'none',
        'can_write_flags': False
    },
    {
        'model_name': 'planner',
        'model_type': 'gemini-1.5-flash-latest',
        'system_instruction': "You are an AI assistant that creates plans based on analyzed requirements. Choose appropriate tools for each step of the plan.",
        'prompt': "Create a detailed plan based on these analyzed requirements: {{previous_responses}}. Choose appropriate tools for each step.",
        'tool_access': 'chooser',
        'can_write_flags': True
    },
    {
        'model_name': 'executor',
        'model_type': 'gemini-1.5-flash-latest',
        'system_instruction': "You are an AI assistant that executes plans using provided tools. Follow the plan step by step and use tools as needed.",
        'prompt': "Execute the following plan: {{previous_responses}}. Use tools as specified in the plan.",
        'tool_access': 'all',
        'can_write_flags': True
    },
    {
        'model_name': 'evaluator',
        'model_type': 'gemini-1.5-flash-latest',
        'system_instruction': "You are an AI assistant that evaluates the results of executed plans. Assess if the original requirements have been met.",
        'prompt': "Evaluate the results of this executed plan: {{previous_responses}}. Have the original requirements been met?",
        'tool_access': 'none',
        'can_write_flags': True
    },
    {
        'model_name': 'summarizer',
        'model_type': 'gemini-1.5-flash-latest',
        'system_instruction': "You are an AI assistant that summarizes the entire process and provides a final response to the user.",
        'prompt': "Summarize the entire process and provide a final response to the user based on: {{previous_responses}}",
        'tool_access': 'none',
        'can_write_flags': True
    }
]

# Call the function to create the Modelium code
create_embeded_modelium_function(model_configs, max_loops=3, output_filename="my_6_model_modelium_function.py")