import os
import google.generativeai as genai
import json
from typing import List, Dict, Callable, Tuple, Any
import logging
import re
from TOOL_MANAGER import ToolManager
import time


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


# --- Color Variables ---
green = Color.OKGREEN
blue = Color.OKBLUE
cyan = Color.OKCYAN

# --- Logging Setup ---
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


# --- Tool Manager Initialization ---
# You'll likely need this part in the main script, not the template
# tool_manager = ToolManager()


def create_embedded_modelium_function(
        model_configs: List[Dict],
        max_loops: int = None,
        output_filename: str = "generated_modelium.py"
) -> None:
    """
    Generates Python code for a Modelium function based on the provided model configurations.

    Args:
        model_configs: A list of dictionaries, each containing the configuration for a model.
        max_loops: The maximum number of loops for the Modelium function.
        output_filename: The name of the file to save the generated code.
    """

    code_template = """
import google.generativeai as genai
import json
from typing import List, Dict, Callable, Tuple, Any
import logging
import os
import re
from TOOL_MANAGER import ToolManager
import time

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

# --- Color Variables ---
green = Color.OKGREEN
blue = Color.OKBLUE
cyan = Color.OKCYAN

# --- Logging Setup ---
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# --- Tool Manager Initialization ---
tool_manager = ToolManager()  

# --- Global Variables ---
previous_responses = []
all_responses = {}
all_results = {}
loop_count = 0
current_loop_responses = []
current_loop_results = []
last_model_output = ""


def print_colored(color: str, text: str) -> None:

    print(color + text + Color.ENDC)


def extract_text_from_response(response: dict) -> str:

    return response.get('content', '')


def INTERPRET_function_calls(response: dict, tool_manager: ToolManager) -> List[str]:

    retrieved_functions_results = []
    if 'tool_code' in response:
        for tool_code in response['tool_code']:
            tool_name = tool_code.get('name')
            tool_args = tool_code.get('args')
            if tool_name and tool_args:
                tool_function = tool_manager.retrieve_tool_by_name(tool_name)
                if tool_function:
                    try:
                        result = tool_function(**tool_args)
                        retrieved_functions_results.append(result)
                        print_colored(Color.OKGREEN, f"Tool '{tool_name}' executed successfully. Result: {result}")
                    except Exception as e:
                       print(e)
    return retrieved_functions_results


def check_stop_flags(response_text: str) -> Tuple[bool, str, str]:

    stop_flags = [
        "**// STOP_FLAG_SUCCESS //**",
        "**// STOP_FLAG_FRUSTRATION_HIGH //**",
        "**// STOP_FLAG_NO_PROGRESS //**",
        "**// STOP_IMMEDIATE //**",
        "**// STOP_SIMPLE //**",
    ]
    for stop_flag in stop_flags:
        if stop_flag in response_text:
            stop_reason = stop_flag.replace('**//', '').replace('//**', '').strip()
            return True, stop_reason, stop_flag
    return False, None, None


def prepare_return(return_type: str, status: str, all_responses: Dict[str, List[str]], all_results: Dict[str, List[str]], current_loop_responses: List[str], current_loop_results: List[str], last_model_output: str, current_step: int) -> Tuple[bool, Dict[str, Any], Dict[str, Any]]:

    results = {
        'status': status,
        'current_step': current_step,
        'last_model_output': last_model_output,
    }
    if return_type == 'all':
        results['all_responses'] = all_responses
        results['all_results'] = all_results
    elif return_type == 'last_output':
        results['last_model_output'] = last_model_output
    elif return_type == 'current_loop':
        results['current_loop_responses'] = current_loop_responses
        results['current_loop_results'] = current_loop_results
    elif return_type == 'simplified':
        results['last_model_output'] = last_model_output
        results['current_step'] = current_step
    return True, results, {}

# --- Model Initialization ---
{model_init_code}

def check_stop_flags(response_text: str) -> Tuple[bool, str, str]:
    # (Keep this function as before)

def prepare_return(return_type: str, status: str, all_responses: Dict[str, List[str]], all_results: Dict[str, List[str]], current_loop_responses: List[str], current_loop_results: List[str], last_model_output: str, current_step: int) -> Tuple[bool, Dict[str, Any], Dict[str, Any]]:
    # (Keep this function as before)

def run_modelium(
    user_input: str,
    max_loops: int = None,
    return_type: str = "all"
) -> Tuple[bool, Dict[str, Any], Dict[str, Any]]:
    previous_responses = []
    all_responses = {{}}
    all_results = {{}}
    loop_count = 0
    current_loop_responses = []
    current_loop_results = []
    last_model_output = ""

    model_configs = [
{model_configs_str}
    ]

    while True:
        if max_loops is not None and loop_count >= max_loops:
            return prepare_return(return_type, "max_loops_reached", all_responses, all_results, 
                                  current_loop_responses, current_loop_results, last_model_output, loop_count)

        loop_count += 1
        current_loop_responses = []
        current_loop_results = []

        for model_config in model_configs:
            model_name = model_config['model_name']
            try:
                # --- Model Interaction ---
                prompt = model_config['prompt'].format(user_input=user_input, previous_responses=previous_responses)
                response = globals()[f"{{model_name}}_chat"].send_message(prompt)

                retrieved_functions_results = INTERPRET_function_calls(response, tool_manager)
                response_text = extract_text_from_response(response)
                print_colored(Color.OKGREEN, f'{{model_name}} Response: {{response_text}}')

                all_responses.setdefault(model_name, []).append(response_text)
                current_loop_responses.append(response_text)
                previous_responses.append(response_text)

                if model_config['tool_access'] == 'all':
                    previous_responses.extend(retrieved_functions_results)
                    all_results.setdefault(f'{{model_name}}_tools', []).extend(retrieved_functions_results)
                    current_loop_results.extend(retrieved_functions_results)

                last_model_output = response_text

                stop_flag_found, stop_reason, stop_flag = check_stop_flags(response_text)

                if stop_flag_found:
                    print(f"Stop flag detected: {{stop_flag}} - {{stop_reason}}")

                    if stop_flag == "**// STOP_IMMEDIATE //**":
                        return prepare_return(return_type, "immediate_stop", all_responses, all_results, 
                                              current_loop_responses, current_loop_results, last_model_output, model_configs.index(model_config) + 1)

                    elif stop_flag == "**// STOP_FLAG_SUCCESS //**":
                        return prepare_return(return_type, "success_stop", all_responses, all_results, 
                                              current_loop_responses, current_loop_results, last_model_output, model_configs.index(model_config) + 1)

                    elif stop_flag in ["**// STOP_SIMPLE //**", "**// STOP_FLAG_FRUSTRATION_HIGH //**", "**// STOP_FLAG_NO_PROGRESS //**"]:
                        # These flags will cause the loop to finish the current iteration before stopping
                        if model_config == model_configs[-1]:
                            return prepare_return(return_type, f"{{stop_reason}}_stop", all_responses, all_results, 
                                                  current_loop_responses, current_loop_results, last_model_output, len(model_configs))

            except Exception as e:
                logger.error(f"Error in modelium execution: {{e}}")
                return False, {{"error": str(e)}}, {{}}

    # This point should not be reached, but including for completeness
    return prepare_return(return_type, "completed", all_responses, all_results, 
                          current_loop_responses, current_loop_results, last_model_output, len(model_configs))

# Example usage
if __name__ == "__main__":
    user_input = input("What would you like to do? ")
    return_type = "all"  # Can be "all", "last_output", "current_loop", or "simplified"
    success, results, function_results = run_modelium(
        user_input, 
        max_loops=5, 
        return_type=return_type
    )

    if success:
        print("Modelium execution successful:")
        print(f"Status: {{results['status']}}")
        if 'all_responses' in results:
            for model, responses in results['all_responses'].items():
                print(f"{{model}}:")
                for response in responses:
                    print(f"  - {{response}}")
        if 'all_results' in results:
            for function, values in results['all_results'].items():
                print(f"{{function}}:")
                for value in values:
                    print(f"  - {{value}}")
        if 'last_model_output' in results:
            print(f"Last model output: {{results['last_model_output']}}")
        if 'current_loop_responses' in results:
            print("Current loop responses:")
            for response in results['current_loop_responses']:
                print(f"  - {{response}}")
        if 'current_step' in results:
            print(f"Stopped at step: {{results['current_step']}}")
    else:
        print("Modelium execution failed:", results["error"])
"""

    # Generate Model Initialization Code
    model_init_code = ""
    model_configs_str = ""
    for model_config in model_configs:
        model_name = model_config['model_name']
        model_type = model_config['model_type']
        tool_access = model_config['tool_access']
        system_instruction = model_config['system_instruction']
        check_flags = model_config.get('check_flags', False)

        # Format tool names for system instruction
        formatted_tools = ""
        if tool_access == 'chooser':
            tools = tool_manager.retrieve_tools_by_names()
            for i, tool in enumerate(tools):
                formatted_tools += f"- **{tool}**: {tools[tool]}\n"

        if tool_access == 'chooser':
            system_instruction += f'''
                You are a helpful and polite AI assistant that will plan and choose the right tools to complete the task.
                You have the following tools available:
                {formatted_tools}
            '''

        if check_flags:
            flag_instruction = '''
            You can control the loop execution by including these flags in your response:
            **// STOP_FLAG_SUCCESS //** : Use when the task is successfully completed.
            **// STOP_FLAG_FRUSTRATION_HIGH //** : Use if you detect high user frustration.
            **// STOP_FLAG_NO_PROGRESS //** : Use if you detect no progress is being made.
            **// STOP_IMMEDIATE //** : Use for immediate termination of the process.
            **// STOP_SIMPLE //** : Use to simply stop the current loop iteration.
            '''
            system_instruction += flag_instruction

        model_init_code += f"{model_name} = genai.GenerativeModel(\n"
        model_init_code += f"    model_name='{model_type}',\n"
        model_init_code += f"    system_instruction=f\"\"\"{system_instruction}\"\"\",\n"

        if tool_access == 'chooser':
            model_init_code += f"    tools=[tool_manager.retrieve_tools_by_names],\n"
        elif tool_access == 'all':
            model_init_code += f"    tools=tool_manager.get_all_tool_functions(),\n"

        model_init_code += ")\n"
        model_init_code += f"{model_name}_chat = {model_name}.start_chat(history=[])\n\n"

        # Add model config to the model_configs_str
        model_configs_str += f"        {{\n"
        for key, value in model_config.items():
            if isinstance(value, str):
                model_configs_str += f"            '{key}': '{value}',\n"
            else:
                model_configs_str += f"            '{key}': {value},\n"
        model_configs_str += f"        }},\n"

    # Create the Final Code
    final_code = code_template.format(
        model_init_code=model_init_code,
        model_configs_str=model_configs_str
    )

    # Write to File
    with open(output_filename, "w") as f:
        f.write(final_code)

    print(f"Modelium function code has been generated and saved to {output_filename}")


# Example usage
model_configs = [
    {
        "model_name": "summarizer",
        "model_type": "gemini-pro",
        "system_instruction": "You are a helpful and concise summarizer.",
        "prompt": "Summarize the following text:\n{{user_input}}",
        "tool_access": "none",
        "check_flags": True
    },
    {
        "model_name": "question_answerer",
        "model_type": "gemini-pro",
        "system_instruction": "You are a question answering expert. Answer the following question based on the provided context.",
        "prompt": "Context:\n{{previous_responses[0]}}\n\nQuestion: {{user_input}}",
        "tool_access": "chooser",
        "check_flags": True
    },
    {
        "model_name": "code_generator",
        "model_type": "gemini-pro",
        "system_instruction": "You are a code generator. Generate Python code based on the provided instructions.",
        "prompt": "Instructions:\n{{user_input}}\n\nGenerate Python code:",
        "tool_access": "all",
        "check_flags": True
    },
    {
        "model_name": "sentiment_analyzer",
        "model_type": "gemini-pro",
        "system_instruction": "You are a sentiment analyzer. Analyze the sentiment of the given text and provide a label (positive, negative, neutral).",
        "prompt": "Analyze the sentiment of this text: \n{{user_input}}\n\nSentiment Label:",
        "tool_access": "none",
        "check_flags": True
    }
]

# Generate the Modelium code
create_embedded_modelium_function(model_configs, max_loops=3, output_filename="generated_modelium.py")