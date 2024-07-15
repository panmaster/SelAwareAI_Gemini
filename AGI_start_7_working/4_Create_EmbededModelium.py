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

    # Template 1: Imports and initial setup
    template1 = textwrap.dedent('''
    import google.generativeai as genai
    import json
    from typing import List, Dict, Callable, Tuple, Any
    import logging
    import os
    import re
    import time
    from TOOL_MANAGER import ToolManager

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

    def print_colored(color: str, text: str) -> None:
        print(f"{color}{text}{Color.ENDC}")

    # Set up logging
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
    logger = logging.getLogger(__name__)

    # Replace with your actual API key
    API_KEY = os.getenv("GOOGLE_API_KEY")
    if not API_KEY:
        raise ValueError("GOOGLE_API_KEY environment variable not set")
    genai.configure(api_key=API_KEY)

    # --- Tool Definitions ---
    tools_folder = "tools"
    tool_manager = ToolManager(tools_folder)
    toolsStr = tool_manager.get_tool_descriptions()

    # Format and sanitize tool descriptions for the planner
    formatted_tools = "\\n".join(f"{i+1}. '{name}' = '{description.strip()}'"
                                 for i, (name, description) in enumerate(toolsStr.items()))

    # --- Helper Functions ---
    def extract_text_from_response(response) -> str:
        return "\\n".join(part.text for candidate in response.candidates
                          for part in candidate.content.parts).strip()

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

    def choose_retrieve_tools_by_names(tool_names: List[str]) -> List[Callable]:
        print("Choosing and retrieving tools...")
        return tool_manager.retrieve_tools_by_names(tool_names) 

    # --- Model Initialization ---
    ''')

    # Template 2: Model initialization
    template2 = ""
    for model_config in model_configs:
        model_name = model_config['model_name']
        model_type = model_config['model_type']
        tool_access = model_config['tool_access']
        system_instruction = model_config['system_instruction']
        check_flags = model_config.get('check_flags', False)

        if tool_access == 'chooser':
            system_instruction += '''
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

        template2 += textwrap.dedent(f'''
        {model_name} = genai.GenerativeModel(
            model_name='{model_type}',
            system_instruction=f"""{system_instruction}""",
            {'tools=[tool_manager.retrieve_tools_by_names],' if tool_access == 'chooser' else ''}
            {'tools=tool_manager.get_all_tool_functions(),' if tool_access == 'all' else ''}
        )
        {model_name}_chat = {model_name}.start_chat(history=[])

        ''')

    # Template 3: Helper functions
    template3 = textwrap.dedent('''
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
    ''')

    # Template 4: Prepare return function
    template4 = textwrap.dedent('''
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
    ''')

    # Template 5: Run Modelium function
    template5 = textwrap.dedent(f'''
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
    ''')

    # Dynamically create the code for the loop, based on model_configs
    for i, model_config in enumerate(model_configs):
        model_name = model_config['model_name']
        prompt = model_config['prompt']
        tool_access = model_config['tool_access']
        check_flags = model_config.get('check_flags', False)

        # Start the chain with the first model and initial user input
        if i == 0:
            template5 += textwrap.dedent(f'''
                # --- {model_name} Stage ---
                print_colored(Color.OKBLUE, f"--- {model_name} Stage ---")
                prompt_{model_name} = f"previous  {{previous_responses}} " 
                prompt_{model_name} += f"""prompt:{prompt}"""
                prompt_{model_name} = prompt_{model_name}.replace("{{user_input}}", user_input)
                {model_name}_response = {model_name}_chat.send_message(prompt_{model_name}, tools=[tool_manager.retrieve_tools_by_names] if "{model_name}" == "Planner" else [])
                ''')
        # Subsequent models in the chain
        else:
            previous_model_name = model_configs[i - 1]['model_name']
            template5 += textwrap.dedent(f'''
                # --- {model_name} Stage ---
                print_colored(Color.OKBLUE, f"--- {model_name} Stage ---")
                prompt_{model_name} = f"""{prompt}"""  # Use the actual 'prompt' value
                prompt_{model_name} = prompt_{model_name}.replace("{{previous_responses}}", '\\n'.join(previous_responses))
                prompt_{model_name} = prompt_{model_name}.replace("{{{previous_model_name}_text}}", {previous_model_name}_text)
                {model_name}_response = {model_name}_chat.send_message(prompt_{model_name}, tools=[tool_manager.retrieve_tools_by_names] if "{model_name}" == "RePlanner" else [])
                ''')

        template5 += textwrap.dedent(f'''
                {model_name}_text = extract_text_from_response({model_name}_response)
                print({model_name}_response)
                print_colored(Color.OKGREEN, f"{model_name}'s Response: {{{model_name}_text}}")
                all_responses.setdefault("{model_name}", []).append({model_name}_text)
        ''')

        if tool_access != 'none':
            template5 += textwrap.dedent(f'''
                {model_name}_results = INTERPRET_function_calls({model_name}_response, tool_manager)
                print_colored(Color.OKCYAN, f"{model_name}'s Function Calls: {{{model_name}_results}}")
                all_results.setdefault("{model_name}", []).extend({model_name}_results)
            ''')

        if check_flags:
                template5 += textwrap.dedent(f'''
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
            ''')

        template5 += textwrap.dedent(f'''
                last_model_output = {model_name}_text
                current_loop_responses.append({model_name}_text)
                previous_responses.append(f"{model_name}: {{{model_name}_text}}")
                current_loop_results.extend({model_name}_results)
        ''')

    template5 += textwrap.dedent('''
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
    ''')

    # Combine all templates
    final_code = template1 + template2 + template3 + template4 + template5

    # Write to File
    with open(output_filename, "w") as f:
        f.write(final_code)

    print(f"Modelium function code has been generated and saved to {output_filename}")

model_configs = [
    {
        "model_name": "Planner",
        "model_type": "gemini-pro",
        "tool_access": "chooser",
        "system_instruction": "You are a strategic planner. Your role is to analyze the task and create a detailed plan of action.",
        "prompt": "Task: {{user_input}}. Please create a detailed plan to accomplish this task. Include steps and any tools that might be needed.",
        "check_flags": True
    },
    {
        "model_name": "Researcher",
        "model_type": "gemini-pro",
        "tool_access": "all",
        "system_instruction": "You are a thorough researcher. Your job is to gather relevant information for the task at hand.",
        "prompt": "Based on the plan: {{Planner_text}}, please research and provide key information needed to execute this plan. Use available tools to gather data.",
        "check_flags": False
    },
    {
        "model_name": "Executor",
        "model_type": "gemini-pro",
        "tool_access": "all",
        "system_instruction": "You are an efficient executor. Your role is to carry out the planned actions using the provided information.",
        "prompt": "Using the plan ({{Planner_text}}) and the research ({{Researcher_text}}), please execute the necessary actions. Describe your actions in detail.",
        "check_flags": True
    },
    {
        "model_name": "Evaluator",
        "model_type": "gemini-pro",
        "tool_access": "none",
        "system_instruction": "You are a critical evaluator. Your job is to assess the outcomes and identify areas for improvement.",
        "prompt": "Evaluate the execution results: {{Executor_text}}. Provide a detailed assessment of the outcomes, highlighting successes and areas for improvement.",
        "check_flags": False
    },
    {
        "model_name": "Optimizer",
        "model_type": "gemini-pro",
        "tool_access": "chooser",
        "system_instruction": "You are an innovative optimizer. Your role is to suggest improvements and optimizations based on the evaluation.",
        "prompt": "Based on the evaluation ({{Evaluator_text}}), please suggest optimizations and improvements to the original plan. If needed, outline a revised plan of action.",
        "check_flags": True
    }
]

# Call the function to generate the Modelium code
create_embedded_modelium_function(
    model_configs=model_configs,
    max_loops=3,
    output_filename="five_stage_modelium.py"
)