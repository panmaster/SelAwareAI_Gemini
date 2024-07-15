# create_Embeded_Modeliuim.py
# this  script  is  en  engine  that  creates a  script, that is in essence an ai   system with  interconected ai  models
# this  scipts is  combines  different  templates,  the combination of  these  templaes  creates creates a BIG TEMPLATE, that will be saved as  scirpt
# that  saved scirpt, is an ai engine

from typing import List, Dict
import textwrap


def create_embedded_modelium_function(
        model_configs: List[Dict],
        max_loops: int = None,
        output_filename="generated_modelium.py"
):
    """
    Generates a Python function that implements a Modelium-like loop.

    Args:
        model_configs: A list of dictionaries, each defining a model to be used in the loop.
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
    def extract_text_from_response(response) -> str:
        return "\\n".join(part.text for candidate in response.candidates
                          for part in candidate.content.parts).strip() 
    """

    # 7. Helper Function: INTERPRET_function_calls
    template_interpret_function_calls = """
    def INTERPRET_function_calls(response, tool_manager: ToolManager) -> List[str]:
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

    # 9. Model Initialization (Dynamic)
    template_model_init = f"""
        {{model_name}} = genai.GenerativeModel(
            model_name='{{model_type}}',
            system_instruction=f\"""{{system_instruction}}\""",
            tools=[tool_manager.retrieve_tools_by_names] if {{tool_access}} == 'chooser' else tool_manager.get_all_tool_functions() if {{tool_access}} == 'all' else None, 
        )
        {{model_name}}_chat = {{model_name}}.start_chat(history=[])
    """

    # 10. Helper Function: check_stop_flags
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

    # 11. Helper Function: prepare_return
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

    # 12. Main Function: run_modelium (Start)
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
    """

    # 13. Model Stage (Dynamic) - First Model
    template_model_stage_first = """
                # --- {model_name} Stage ---
                print_colored(Color.OKBLUE, f"--- {model_name} Stage ---")
                prompt_{model_name} = f"previous  {{previous_responses}} " 
                prompt_{model_name} += f\"""prompt:{prompt}\"""
                prompt_{model_name} = prompt_{model_name}.replace("{{user_input}}", user_input)
                {model_name}_response = {model_name}_chat.send_message(prompt_{model_name}, tools=[tool_manager.retrieve_tools_by_names] if "{model_name}" == "Planner" else [])
    """

    # 14. Model Stage (Dynamic) - Subsequent Models
    template_model_stage_subsequent = """
                # --- {model_name} Stage ---
                print_colored(Color.OKBLUE, f"--- {model_name} Stage ---")
                prompt_{model_name} = f\"""{prompt}\""" 
                prompt_{model_name} = prompt_{model_name}.replace("{{previous_responses}}", '\\n'.join(previous_responses))
                prompt_{model_name} = prompt_{model_name}.replace("{{{previous_model_name}_text}}", {previous_model_name}_text)
                {model_name}_response = {model_name}_chat.send_message(prompt_{model_name}, tools=[tool_manager.retrieve_tools_by_names] if "{model_name}" == "RePlanner" else [])
    """

    # 15. Model Response Handling (Dynamic)
    template_model_response_handling = """
                {model_name}_text = extract_text_from_response({model_name}_response)
                print({model_name}_response)
                print_colored(Color.OKGREEN, f"{model_name}'s Response: {{{model_name}_text}}")
                all_responses.setdefault("{model_name}", []).append({model_name}_text)
    """

    # 16. Tool Usage Handling (Dynamic)
    template_tool_usage = """
                {model_name}_results = INTERPRET_function_calls({model_name}_response, tool_manager)
                print_colored(Color.OKCYAN, f"{model_name}'s Function Calls: {{{model_name}_results}}")
                all_results.setdefault("{model_name}", []).extend({model_name}_results)
    """

    # 17. Stop Flag Check (Dynamic)
    template_stop_flag_check = """
                stop_flag, reason, flag = check_stop_flags({model_name}_text)
                if stop_flag:
                    print_colored(Color.WARNING, f"Loop stopped due to flag: {{flag}} (Reason: {{reason}})")
                    if flag == "**// STOP_SIMPLE //**":
                        continue  # Continue to the next loop iteration
                    else:
                        return prepare_return(
                            return_type=return_type,
                            status=reason,
                            all_responses=all_responses,
                            all_results=all_results,
                            current_loop_responses=current_loop_responses,
                            current_loop_results=current_loop_results,
                            last_model_output={model_name}_text,
                            current_step=loop_count
                        )
    """

    # 18. Response and Result Collection (Dynamic)
    template_collect_responses = """
                last_model_output = {model_name}_text
                current_loop_responses.append({model_name}_text)
                previous_responses.append(f"{model_name}: {{{model_name}_text}}")
                current_loop_results.extend({model_name}_results)
    """

    # 19. Main Function: run_modelium (End)
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
            template_run_modelium_start
    )

    # --- Add Dynamic Model Parts ---
    for i, model_config in enumerate(model_configs):
        model_name = model_config['model_name']
        model_type = model_config['model_type']
        tool_access = model_config['tool_access']
        system_instruction = model_config['system_instruction']
        prompt = model_config['prompt']
        check_flags = model_config.get('check_flags', False)

        if tool_access == 'chooser':
            system_instruction += """
            You are a helpful and polite AI assistant that will plan and choose the right tools to complete the task.
            You have the following tools available:
            {formatted_tools}
            """

        if check_flags:
            flag_instruction = """
            You can control the loop execution by including these flags in your response:
            **// STOP_FLAG_SUCCESS //** : Use when the task is successfully completed.
            **// STOP_FLAG_FRUSTRATION_HIGH //** : Use if you detect high user frustration.
            **// STOP_FLAG_NO_PROGRESS //** : Use if you detect no progress is being made.
            **// STOP_IMMEDIATE //** : Use for immediate termination of the process.
            **// STOP_SIMPLE //** : Use to simply stop the current loop iteration.
            """
            system_instruction += flag_instruction

        final_code += f"""
            {template_model_init.format(model_name=model_name,
                                         model_type=model_type,
                                         system_instruction=system_instruction,
                                         tool_access=tool_access)}
        """

        if i == 0:
            final_code += template_model_stage_first.format(model_name=model_name, prompt=prompt)
        else:
            previous_model_name = model_configs[i - 1]['model_name']
            final_code += template_model_stage_subsequent.format(model_name=model_name,
                                                                 prompt=prompt,
                                                                 previous_model_name=previous_model_name)

        final_code += template_model_response_handling.format(model_name=model_name)

        if tool_access != 'none':
            final_code += template_tool_usage.format(model_name=model_name)

        if check_flags:
            final_code += template_stop_flag_check.format(model_name=model_name)

        final_code += template_collect_responses.format(model_name=model_name)

    # Complete the run_modelium function
    final_code += template_run_modelium_end

    # Write to File
    with open(output_filename, "w") as f:
        f.write(final_code)

    print(f"Modelium function code generated and saved to {output_filename}")

# Example Function Call
# (Make sure you have the TOOL_MANAGER.py file defined and your API key in place)
if __name__ == "__main__":
    model_configs = [
        {
            "model_name": "Goal Setter",
            "model_type": "gemini-pro",
            "tool_access": "none",
            "system_instruction": "Clearly define the main goal given the user input.",
            "prompt": "User Input: {{user_input}}\\nMain Goal:",
            "check_flags": False
        },
        {
            "model_name": "Planner",
            "model_type": "gemini-pro",
            "tool_access": "chooser",
            "system_instruction": "You are a strategic planner. Create a detailed plan to achieve the goal.",
            "prompt": "Goal: {{Goal_Setter_text}}\\nDetailed Plan:",
            "check_flags": True
        }

    ]
    create_embedded_modelium_function(model_configs=model_configs, output_filename="modelium_example.py")

