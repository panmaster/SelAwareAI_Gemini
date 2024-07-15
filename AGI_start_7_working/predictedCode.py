import google.generativeai as genai
import json
from typing import List, Dict, Callable, Tuple, Any
import logging
import os
import time
from TOOL_MANAGER import ToolManager


# --- ANSI Color Codes ---
class Color:
    HEADER = '\033[95m'  # Corrected ANSI escape code format
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


def print_colored(color: str, text: str) -> None:
    print(f"{color}{text}{Color.ENDC}")


# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Replace with your actual Google API key
API_KEY = os.getenv("GOOGLE_API_KEY")
if not API_KEY:
    raise ValueError("GOOGLE_API_KEY environment variable not set")
genai.configure(api_key=API_KEY)

# --- Tool Definitions ---
tools_folder = "tools"
tool_manager = ToolManager(tools_folder)
toolsStr = tool_manager.get_tool_descriptions()

# Format and sanitize tool descriptions
formatted_tools = "\n".join(f"{i + 1}. '{name}' = '{description.strip()}'"
                            for i, (name, description) in enumerate(toolsStr.items()))


def extract_text_from_response(response) -> str:
    extracted_text = ""
    for candidate in response.candidates:
        for part in candidate.content.parts:
            extracted_text += part.text
    return extracted_text.strip()


def INTERPRET_function_calls(response, tool_manager: ToolManager) -> List[str]:
    results = []
    for candidate in response.candidates:
        for part in candidate.content.parts:
            function_call = getattr(part, 'function_call', None)
            if function_call:
                print_colored(Color.OKBLUE, "---------------INTERPRETER-------------------")
                tool_name = function_call.name

                # Simplified tool retrieval
                tool_function = tool_manager.get_tool_function(tool_name)

                if not tool_function:
                    logger.warning(f"Tool function '{tool_name}' not found.")
                    continue

                function_args = {arg_name: arg_value for arg_name, arg_value in function_call.args.items()}

                print(f"Function name: {Color.OKGREEN}{tool_name}{Color.ENDC}")
                for key, value in function_args.items():
                    print(f"        {Color.OKCYAN}{key}{Color.ENDC}: {value}")

                try:
                    result = tool_function(**function_args)
                    results.append(result)
                except Exception as e:
                    error_msg = f"Error calling {tool_name}: {e}"
                    logger.error(error_msg)
                    results.append(error_msg)

    return results


def check_stop_flags(response_text: str) -> Tuple[bool, str, str]:
    stop_flags = {
        "**// STOP_FLAG_SUCCESS //**": "success",
        "**// STOP_FLAG_FRUSTRATION_HIGH //**": "frustration",
        "**// STOP_FLAG_NO_PROGRESS //**": "no_progress",
        "**// STOP_IMMEDIATE //**": "immediate",
        "**// STOP_SIMPLE //**": "simple"
    }

    for flag, reason in stop_flags.items():
        if flag in response_text:
            return True, reason, flag
    return False, "", ""


def prepare_return(
        return_type: str,
        status: str,
        all_responses: Dict[str, List[str]],
        all_results: Dict[str, List[str]],
        current_loop_responses: List[str],
        current_loop_results: List[str],
        last_model_output: str,
        current_step: int
) -> Tuple[bool, Dict[str, Any], Dict[str, Any]]:
    if return_type == "all":
        return True, {"status": status, "all_responses": all_responses, "all_results": all_results}, {}
    elif return_type == "last_output":
        return True, {"status": status, "last_model_output": last_model_output}, {}
    elif return_type == "current_loop":
        return True, {"status": status, "current_loop_responses": current_loop_responses}, {
            "current_loop_results": current_loop_results}
    elif return_type == "simplified":
        return True, {"status": status, "last_output": last_model_output, "current_step": current_step}, {}
    else:
        return True, {"status": status, "all_responses": all_responses, "all_results": all_results}, {}


def run_modelium(
        user_input: str,
        model_configs: List[Dict[str, str]],  # Pass model configurations
        max_loops: int = None,
        return_type: str = "all"
) -> Tuple[bool, Dict[str, Any], Dict[str, Any]]:
    previous_responses = []
    all_responses = {}
    all_results = {}
    loop_count = 0
    current_loop_responses = []
    current_loop_results = []
    last_model_output = ""

    # --- Model Initialization Outside the Loop ---
    model_chats = {}  # Store initialized chat objects
    for model_config in model_configs:
        model_name = model_config['model_name']
        # Access tool access setting for each model
        tool_access = model_config.get('tool_access', 'none')
        tools = None
        if tool_access == 'chooser':
            tools = [tool_manager.retrieve_tools_by_names]
        elif tool_access == 'all':
            tools = tool_manager.get_all_tool_functions()

        model = genai.GenerativeModel(
            model_name=model_config['model_name'],
            system_instruction=model_config['system_instruction'],
            tools=tools
        )
        model_chats[model_name] = model.start_chat(history=[])

    while True:
        loop_count += 1
        if max_loops is not None and loop_count > max_loops:
            print_colored(Color.WARNING, f"Reached maximum loop count: {max_loops}")
            return prepare_return(
                return_type=return_type,
                status="max_loops_reached",
                all_responses=all_responses,
                all_results=all_results,
                current_loop_responses=current_loop_responses,
                current_loop_results=current_loop_results,
                last_model_output=last_model_output,
                current_step=loop_count
            )

            # --- Dynamic Model Execution within the Loop ---
        for i, model_config in enumerate(model_configs):
            model_name = model_config['model_name']
            # --- Model Stage ---
            print_colored(Color.OKBLUE, f"--- {model_name} Stage ---")
            if i == 0:
                prompt = f"previous responses: {previous_responses}" + model_config['prompt']
                prompt = prompt.replace("{{user_input}}", user_input)
            else:
                prompt = model_config['prompt']
                prompt = prompt.replace("{{previous_responses}}", " ".join(previous_responses))
                # Access previous model's output using the model name
                prompt = prompt.replace(f"{{{{{model_configs[i - 1]['model_name']}_text}}}}",
                                        eval(f"model_configs[{i - 1}]['model_name'] + '_text'"))

            # --- Execute Model ---
            # Use the initialized chat object from the dictionary
            response = model_chats[model_name].send_message(prompt)
            text = extract_text_from_response(response)
            print(response)
            print_colored(Color.OKGREEN, f"{model_name}'s Response: {text}")

            # --- Store Model Output for Next Stage ---
            globals()[model_name + '_text'] = text  # Dynamically create variable

            all_responses.setdefault(model_name, []).append(text)

            results = INTERPRET_function_calls(response, tool_manager)
            print_colored(Color.OKCYAN, f"{model_name}'s Function Calls: {results}")
            all_results.setdefault(model_name, []).extend(results)
            last_model_output = text
            current_loop_responses.append(text)
            previous_responses.append(f"{model_name}: {text}")
            current_loop_results.extend(results)

            stop_flag, reason, _ = check_stop_flags(text)
            if stop_flag:
                print_colored(Color.WARNING, f"Loop stopped because stop flag was detected")
                return prepare_return(
                    return_type=return_type,
                    status=reason,
                    all_responses=all_responses,
                    all_results=all_results,
                    current_loop_responses=current_loop_responses,
                    current_loop_results=current_loop_results,
                    last_model_output=last_model_output,
                    current_step=loop_count
                )

        time.sleep(1)  # Add a delay to avoid rate limiting
        return prepare_return(
            return_type=return_type,
            status="success",
            all_responses=all_responses,
            all_results=all_results,
            current_loop_responses=current_loop_responses,
            current_loop_results=current_loop_results,
            last_model_output=last_model_output,
            current_step=loop_count
        )