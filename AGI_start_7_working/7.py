from typing import List, Dict
import textwrap

def create_embedded_modelium_function(
    model_configs: List[Dict],
    max_loops: int = None,
    output_filename="generated_modelium.py"
):
    """
    Generates a Python function that implements a Modelium-like loop, dynamically chaining models.

    Args:
        model_configs: A list of dictionaries, each defining a model to be used in the loop.
            Each dictionary should have the following keys:
                - "model_name": The name of the model (used in variables and prompts).
                - "model_type": The model type (e.g., "gemini-pro").
                - "tool_access": How the model accesses tools: "none", "chooser", or "all".
                - "system_instruction": The system instructions for the model.
                - "prompt": The model's prompt template (can use placeholders).
                - "check_flags": (Optional) Whether to check for stop flags in the model's output.
        max_loops: Maximum number of loops to run. If None, the loop continues indefinitely.
        output_filename: Name of the file to save the generated code.
    """

    # --- Templates ---

    # 1. Imports and Constants
    template_imports = """
    import google.generativeai as genai
    import json
    from typing import List, Dict, Callable, Tuple, Any
    import logging
    import os
    import time
    from TOOL_MANAGER import ToolManager 
    """

    # 2. ANSI Color Codes
    template_colors = """
    # --- ANSI Color Codes ---
    class Color:
        HEADER = r'\033[95m'
        OKBLUE = r'\033[94m'
        OKCYAN = r'\033[96m'
        OKGREEN = r'\033[92m'
        WARNING = r'\033[93m'
        FAIL = r'\033[91m'
        ENDC = r'\033[0m'
        BOLD = r'\033[1m'
        UNDERLINE = r'\033[4m' 

    def print_colored(color: str, text: str) -> None:
        print(f"{color}{text}{Color.ENDC}")
    """

    # 3. Logging Setup
    template_logging = """
    # Set up logging
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
    logger = logging.getLogger(__name__) 
    """

    # 4. API Key Setup
    template_api_key = """
    # Replace with your actual Google API key
    API_KEY = os.getenv("GOOGLE_API_KEY")
    if not API_KEY:
        raise ValueError("GOOGLE_API_KEY environment variable not set")
    genai.configure(api_key=API_KEY)
    """

    # 5. Tool Manager Setup
    template_tool_manager = """
    # --- Tool Definitions ---
    tools_folder = "tools"
    tool_manager = ToolManager(tools_folder)
    toolsStr = tool_manager.get_tool_descriptions()

    # Format and sanitize tool descriptions 
    formatted_tools = "\\n".join(f"{i+1}. '{name}' = '{description.strip()}'"
                                 for i, (name, description) in enumerate(toolsStr.items()))
    """

    # 6. Helper Function: extract_text_from_response
    template_extract_text = """
    def extract_text_from_response(response, model_config) -> str:  
        extracted_text = ""
        for candidate in response.candidates:
            for part in candidate.content.parts:
                extracted_text += part.text
        return extracted_text.strip()
    """

    # 7. Helper Function: INTERPRET_function_calls
    template_interpret_function_calls = """
    def INTERPRET_function_calls(response, tool_manager: ToolManager, model_config) -> List[str]:  
        results = []
        for candidate in response.candidates:
            for part in candidate.content.parts:
                function_call = getattr(part, 'function_call', None)
                if function_call:
                    print_colored(Color.OKBLUE, "---------------INTERPRETER-------------------")
                    tool_name = function_call.name
                    tool_function = (tool_manager.retrieve_tools_by_names 
                                     if tool_name == 'retrieve_tools_by_names' 
                                     else tool_manager.get_tool_function(tool_name)) 

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
    """

    # 8. Helper Function: choose_retrieve_tools_by_names
    template_choose_tools = """
    def choose_retrieve_tools_by_names(tool_names: List[str]) -> List[Callable]:
        print("Choosing and retrieving tools...")
        return tool_manager.retrieve_tools_by_names(tool_names)  
    """

    # 9. Helper Function: check_stop_flags
    template_check_flags = """
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
    """

    # 10. Helper Function: prepare_return
    template_prepare_return = """
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
            return True, {"status": status, "current_loop_responses": current_loop_responses}, {"current_loop_results": current_loop_results}
        elif return_type == "simplified":
            return True, {"status": status, "last_output": last_model_output, "current_step": current_step}, {}
        else:
            return True, {"status": status, "all_responses": all_responses, "all_results": all_results}, {}
    """

    # --- Main Function: run_modelium (Split into Start, Middle, End) ---

    # Start Template
    template_run_modelium_start = f"""
    def run_modelium(
        user_input: str,
        max_loops: int = {max_loops},
        return_type: str = "all"
    ) -> Tuple[bool, Dict[str, Any], Dict[str, Any]]:
        previous_responses = []
        all_responses = {{}}
        all_results = {{}}
        loop_count = 0
        current_loop_responses = []
        current_loop_results = []
        last_model_output = ""
        feedback=""

        # --- Model Initialization Outside the Loop ---  but  that  model  initaisliation should  be acctual a  laap intiasliaton
        
        this is  wrogn, it  should be  for modelconfin in modecongis()
                                                initialsie  moels!
        
        {  # Begin Model Initialization
            "".join([
                f"""
                {model_config['model_name']} = genai.GenerativeModel(
                    model_name='{model_config['model_type']}',
                    system_instruction=f\"""{model_config['system_instruction']}
                """ + 
                ("""
                    You are a helpful and polite AI assistant that will plan and choose the right tools to complete the task.
                    You have the following tools available:
                    {formatted_tools}
                    """ if model_config['tool_access'] == 'chooser' else "") +
                f"""\""",
                    tools=[tool_manager.retrieve_tools_by_names] if '{model_config['tool_access']}' == 'chooser' else tool_manager.get_all_tool_functions() if '{model_config['tool_access']}' == 'all' else None,
                )
                {model_config['model_name']}_chat = {model_config['model_name']}.start_chat(history=[]) 
                """
                for model_config in model_configs
            ])
        }  # End Model Initialization

        while True:
            loop_count += 1
            if max_loops is not None and loop_count > max_loops:
                print_colored(Color.WARNING, f"Reached maximum loop count: {{max_loops}}")
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
    """

    # Middle Template (Dynamically Generated for Each Model)
    template_run_modelium_middle = f""" 
           
                if i == 0:
                    prompt = f"previous responses: {{feedback}}" + model_config  [0]  ['prompt'] 
                    prompt = " " user_input {{user_input}})
                 """
                for i,model_config,in  enumerate(model_configs):
                    template_run_modelium_middle+="response = eval(f"{model_config['model_name']}_chat.send_message(prompt, tools=[tool_manager.retrieve_tools_by_names] if model_config['tool_access'] == 'chooser' else [])")
                    template_run_modelium_middle+='text = extract_text_from_response(response, model_config)'
                    template_run_modelium_middle+=' print(response)'
                    template_run_modelium_middle +=" results = INTERPRET_function_calls(response, tool_manager, model_config)"

                    template_run_modelium_middle=""""""
                    if 'check_flags' in model_config and model_config['check_flags']:
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
                                )""""""
    """

    # End Template
    template_run_modelium_end = """
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
    """

    # --- Combine Templates ---

    # Start with the main function start
    final_code = template_run_modelium_start

    # Dynamically add the middle template for each model
    for i, model_config in enumerate(model_configs):
        final_code += template_run_modelium_middle.format(model_config=model_config, model_configs=model_configs)

    # Add the main function end
    final_code += template_run_modelium_end

    # Add the other templates (imports, helper functions, etc.)
    final_code = (
        template_imports +
        template_colors +
        template_logging +
        template_api_key +
        template_tool_manager +
        template_extract_text +
        template_interpret_function_calls +
        template_choose_tools +
        template_check_flags +
        template_prepare_return +
        final_code
    )

    # --- Write to File ---
    with open(output_filename, "w") as f:
        f.write(final_code)

    print(f"Modelium function code generated and saved to {output_filename}")


# --- Example Function Call ---
if __name__ == "__main__":
    model_configs = [
        {
            "model_name": "Goal_Setter",
            "model_type": "gemini-pro",
            "tool_access": "none",
            "system_instruction": "Clearly define the main goal given the user input.",
            "prompt": "User Input: {{user_input}}\nMain Goal:",
            "check_flags": False
        },
        {
            "model_name": "Planner",
            "model_type": "gemini-pro",
            "tool_access": "chooser",
            "system_instruction": "You are a strategic planner. Create a detailed plan to achieve the goal.",
            "prompt": "Goal: {{{Goal_Setter_text}}}\nDetailed Plan:",
            "check_flags": True
        }
    ]
    create_embedded_modelium_function(model_configs=model_configs, output_filename="modelium_example.py")