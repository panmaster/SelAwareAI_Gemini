import os
import datetime
import json
import time
import json
from google.protobuf import json_format
from IPython.display import display, Markdown, clear_output
from rich.console import Console
import google.generativeai as genai
from prettytable import PrettyTable
import json
from MEMORY______________frame_creation import CREATE_MEMORY_FRAME as CREATE_MEMORY_FRAME
from Tool_Manager import ToolManager
import  traceback


# Run the function



genai.configure(api_key='AIzaSyA60tGw6fZwQdamW8sm6pkgRh5W559kLJ0')  # Replace with your actual API key

SESSION_FOLDER = "sessions"
MEMORY_FOLDER = "memories"
MEMORY_STRUCTURE_SUMMARY_FILE = "memory_structure_summary.txt"

# ANSI escape codes for colors
RED = "\033[91m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
BLUE = "\033[94m"
MAGENTA = "\033[95m"
CYAN = "\033[96m"
RESET = "\033[0m"
PURPLE = '\033[95m'
BRIGHT_RED = "\033[91m"
BRIGHT_GREEN = "\033[92m"
BRIGHT_YELLOW = "\033[93m"
BRIGHT_BLUE = "\033[94m"
BRIGHT_MAGENTA = "\033[95m"
BRIGHT_CYAN = "\033[96m"


def Load_state_of_mind():
    """
    Loads the state from 'State_of_mind.json' file.

    Returns:
        dict: The loaded state of mind, or None if an error occurred.
    """
    script_dir = os.path.dirname(os.path.abspath(__file__))
    path = os.path.abspath(os.path.join(script_dir, 'Brain_settings/State_of_mind.json'))

    print(f"\n{GREEN}****************  LOADING STATE OF MIND  for  REFLECTION step *******************{RESET}\n")

    try:
        with open(path, 'r') as f:
            state_of_mind = json.load(f)
        print(f"{GREEN}Loaded state of mind:{RESET}")
        print(json.dumps(state_of_mind, indent=4))

        print(f"\n{GREEN}****************  FINISHED LOADING STATE OF MIND  *******************{RESET}\n")
        return state_of_mind
    except Exception as E:
        print(f"Failed to load Load_state_of_mind: {E}")
        return None



def create_session_name_and_path():
    current_directory = os.getcwd()
    sessions_folder = os.path.join(current_directory, "SESIONS")
    session_time = datetime.datetime.now()
    session_time_formatted = session_time.strftime("%H-%M-%S")
    session_name = "Sesion_" + session_time_formatted
    session_path = os.path.join(sessions_folder, session_name)
    os.makedirs(session_path, exist_ok=True)
    return {'session_name': session_name, 'session_path': session_path}


import json
from google.protobuf import json_format




def dict_to_pretty_string(dictionary):
    return json.dumps(dictionary, indent=4)
def sanitize_time_string(time_str: str) -> str:
    return "".join(char for char in time_str if char.isalnum() or char in ("_", "-"))


def create_session_folder() -> str:
    session_timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    session_name = f"session_{session_timestamp}"
    session_path = os.path.join(SESSION_FOLDER, session_name)
    os.makedirs(session_path, exist_ok=True)
    return session_path


def summarize_memory_folder_structure(output_file: str = MEMORY_STRUCTURE_SUMMARY_FILE) -> str:
    memory_path = MEMORY_FOLDER
    summary = ""
    for root, dirs, files in os.walk(memory_path):
        relative_path = os.path.relpath(root, memory_path)
        summary += f"{relative_path}\n"
        for dir in sorted(dirs):
            summary += f"  - {dir}\n"
        for file in sorted(files):
            summary += f"    - {file}\n"

    with open(output_file, "w", encoding="utf-8") as f:
        f.write(summary)
    return summary


def gather_introspection_data(
        action_response_text_back_to_top: str ="None",
        user_input: str = "None",
        memory_summary: str = "None",
        function_call_results: str = "None",
        user_input_signal: str = "None",
        visual_input_signal: str = "None",
        audio_input_signal: str = "None",
) -> list[str]:
    current_time = datetime.datetime.now().strftime("%H:%M:%S")



    introspection_data = [
        f"{current_time}  {action_response_text_back_to_top}     {user_input}",
        f"{function_call_results}",
        "..--->...",
        "What are my available tools and resources?",
        f"Current sensory input (Image, Audio, Text): {visual_input_signal}, {audio_input_signal}, {user_input_signal}",
        "Are there any ongoing short-term tasks?",
        "Are there any long-term ongoing tasks or plans?",

        "1.What is my current goal?",
        "2.What do I want?",
        "3.What am I feeling?",
        "4.What do I need?",
        "5.What am I experiencing?",
        "8.Emotional state?.....",
         " Maybe?  ??",
    ]
    return introspection_data


def perform_reflection(introspection_results: str, STATE_OF_MIND: dict) -> str:  # STATE_OF_MIND is now a dictionary
    current_time = datetime.datetime.now().strftime("%H:%M:%S")
    reflection_prompt = f"""{current_time}

        {introspection_results}
        "internal state: {json.dumps(STATE_OF_MIND, indent=4)}"  # Use json.dumps to format the dictionary nicely
        user is  system, Me is you,
        1. What is  current focus?,
        2. Should  set a new goal? If so, what is it? If not, why not?,
        3. Are there any problems, unknowns, or paradoxes in my memory?,
        4. What problems need to be solved?,
        5. What are possible courses of action based on available information?,
        6. Approach the next steps?:
           a) Think step-by-step?
           b) Focus on a specific aspect?
           c) Defocus and broaden my attention?
           e) If focus YES, Write at  the end what  you are focusing on,
        7. Should I be more verbose in my responses? (Yes/No),
        8. Should I be less verbose? (Yes/No),
        9. Should I change the subject or keep discussing this? (Yes/No),
        10. Should I summarize the current discussion? (Yes/No),
        11. Should I dive deeper into a specific topic? (Yes/No),
        12. Should I store any of this information in my long-term memory (Yes/No)? ,
        13. Should I query my memory for relevant information? (Yes/No),
        14. What is the status of my current goals? ,
    """
    return reflection_prompt


def plan_actions(reflection_results: str) -> str:
    current_time = datetime.datetime.now().strftime("%H:%M:%S")
    action_prompt = f"{current_time} -  Based on this reflection: \n{reflection_results}\nPlan my next actions."
    return action_prompt


def store_conversation_frame(
        introspection_results: str,
        reflection_results: str,
        action_plan: str,
        function_call_results: str,
):
    current_conversation_frame = (
        f"Introspection:\n{introspection_results}\n"
        f"Reflection:\n{reflection_results}\n"
        f"Action Plan:\n{action_plan}\n"
        f"Function Call Results:\n{function_call_results}\n"
    )
    CREATE_MEMORY_FRAME(current_conversation_frame)


def log_conversation(
        conversation_log_path: str,
        iteration_count: int,
        current_conversation_frame: str,
):
    current_time = datetime.datetime.now().strftime("%H:%M:%S")
    with open(conversation_log_path, "a+", encoding="utf-8") as log_file:
        log_file.write(f"--- Awareness Loop: {iteration_count} ---\n")
        log_file.write(f"Time: {current_time}\n")
        log_file.write(current_conversation_frame)
        log_file.write("-" * 20 + "\n\n")

import json
from google.protobuf import json_format


import json

def RESPONSE_INTERPRETER_FOR_FUNCTION_CALLING(response, tool_manager):
    """Interprets the model's response, extracts function details, executes the appropriate functions,
    and gathers results."""
    print()
    print(f"{BLUE}---------------------------RESPONSE_INTERPRETER_FOR_FUNCTION_CALLING-------------------------------")

    Multiple_ResultsOfFunctions_From_interpreter = []

    def process_function_call(function_call):
        function_name = function_call.name
        function_args = function_call.args

        print(f"{BRIGHT_BLUE}Function Call name: {MAGENTA}{function_name}")
        print(f"{BRIGHT_BLUE}Function Call args:")
        for arg_name, arg_value in function_args.items():
            print(f"  {YELLOW}{arg_name}: {arg_value}")

        function_to_call = tool_manager.tool_mapping.get(function_name)

        if function_to_call:
            try:
                results = function_to_call(**function_args)
                modified_results = f"Result of Called function {function_name}: {results}"
                print(f"Result of function: {results}")
                Multiple_ResultsOfFunctions_From_interpreter.append(modified_results)
            except Exception as e:
                error_message = f"Failed to call function {function_name}: {str(e)}"
                print(error_message)
                Multiple_ResultsOfFunctions_From_interpreter.append(error_message)
        else:
            error_message = f"Warning: Tool function '{function_name}' not found."
            print(error_message)
            Multiple_ResultsOfFunctions_From_interpreter.append(error_message)

    def process_content(content):
        if hasattr(content, 'parts'):
            for part in content.parts:
                if hasattr(part, 'function_call'):
                    process_function_call(part.function_call)
        elif hasattr(content, 'function_call'):
            process_function_call(content.function_call)

    # Handle different response structures
    if hasattr(response, 'result'):
        response = response.result

    if hasattr(response, 'candidates'):
        for candidate in response.candidates:
            if hasattr(candidate, 'content'):
                process_content(candidate.content)
    elif hasattr(response, 'content'):
        process_content(response.content)
    elif isinstance(response, dict):
        if 'candidates' in response:
            for candidate in response['candidates']:
                if 'content' in candidate:
                    process_content(candidate['content'])
        elif 'content' in response:
            process_content(response['content'])

    print(f"{BLUE}-------END--------RESPONSE_INTERPRETER_FOR_FUNCTION_CALLING END-------------END---------- ")
    print()
    print()
    return Multiple_ResultsOfFunctions_From_interpreter
def main():
    session_info = create_session_name_and_path()
    session_path = session_info['session_path']
    conversation_log_path = os.path.join(session_path, "conversation_log.txt")
    tool_manager = ToolManager()
    tools_list_json = tool_manager.get_tools_list_json()
    iteration_count = 0
    user_input_count = 0
    function_call_results = ""
    current_conversation_frame = ""
    user_input_signal = "None"
    visual_input_signal = "None"
    audio_input_signal = "None"
    str_function_call_results = ""
    action_response_text_back_to_top = ""



    print(f"\n\033[96mLoaded Tool Descriptions (JSON):\n\033[0m")
    for i, tool_json in enumerate(tools_list_json):
        print(f"  \033[94m{i + 1}. \033[0m{tool_json}")

    print(f"\n\033[96mAll Tool Functions (Mapping):\n\033[0m")
    for tool_name, tool_function in tool_manager.tool_mapping.items():
        print(f"  \033[94m{tool_name}: \033[0m{tool_function}")

    print(f"\n\033[96mShort Tool Descriptions:\n\033[0m")
    for tool_name, short_description in tool_manager.short_descriptions.items():
        print(f"  \033[94m{tool_name}: \033[0m{short_description}")




    available_tools = tool_manager.get_tools_list_json()
    print(available_tools)
    print("prompt init")
    system_instruction_input= """ And  then God  created  shy and  heavesm and  he  made  them  in his  picture,,,,
        """

    system_instruction_reflection= """ 
        user is  assistant and  system,  
        you answer the questions,
        """

    system_instruction_action = """
         Based on coversation  you decided  wether to call function, reponse with text, or do both, you focus  on achiving goals!, you try  your  harders to ....
               """
    with open(conversation_log_path, "a+", encoding="utf-8") as file:
        file.write(f"system_instruction_input: {system_instruction_input}\n")
        file.write(f" system_instruction_reflection: { system_instruction_reflection}\n")
        file.write(f"system_instruction_action: {system_instruction_action}\n")
    print("model init")
    try:
        # Initialize models
        introspection_model = genai.GenerativeModel(
            system_instruction=system_instruction_input,
            model_name="gemini-1.5-flash-latest",
            safety_settings={"HARASSMENT": "block_none"},
            tools=available_tools,
            tool_config={'function_calling_config': 'NONE'}
        )

        introspection_chat = introspection_model.start_chat(history=[])



        time.sleep(0.5)
        reflection_model = genai.GenerativeModel(
            system_instruction=system_instruction_reflection,
            model_name="gemini-1.5-flash-latest",
            safety_settings={"HARASSMENT": "block_none"},

            tools=available_tools,
            tool_config={'function_calling_config': 'NONE'}

        )

        reflection_chat = reflection_model.start_chat(history=[])



        time.sleep(0.5)
        action_model = genai.GenerativeModel(
            system_instruction=system_instruction_action,
            model_name="gemini-1.5-flash-latest",
            safety_settings={"HARASSMENT": "block_none"},
            tools=available_tools,
        )
        action_chat = action_model.start_chat(history=[])



    except Exception as E:
        print(E)
        print("Problems with model initialisations")

    user_input=""
    while True:
        print()
        try:
            if iteration_count % 20 == 0:
                user_input = input(f"{YELLOW}Enter your input (or press Enter to skip): {RESET}")
                user_input_count += 1
            else:
                user_input = ""

            iteration_count += 1


            print()
            print(f"{GREEN}    ****************************** Awareness Loop ******************************    {RESET}")
            print(f"{GREEN}Awareness Loop: {iteration_count}{RESET}")
            function_call_results = str_function_call_results
            memory_summary = summarize_memory_folder_structure()
            #print(memory_summary)

            introspection_data = gather_introspection_data(
                action_response_text_back_to_top,
                user_input,
                memory_summary,
                function_call_results,
                user_input_signal,
                visual_input_signal,
                audio_input_signal,
            )

            print(f"{YELLOW}inputs:")
            print(f"{BLUE}INTROSPECTION input:")
            # =========================input introspection
            try:
                introspection_response = introspection_chat.send_message(introspection_data)

                if introspection_response.text is not None:
                    print(f"{BLUE}{introspection_response.text}")
                    with open(conversation_log_path, "a+", encoding="utf-8") as file:
                        file.write(f"Introspection: {introspection_response.text}\n")


            except Exception as E:
                print(E)



            print()
            print(f"{GREEN}Reflection:{GREEN}")

            # =========================relection
            STATE_OF_MIND=""
            try:
                STATE_OF_MIND= Load_state_of_mind()
            except Exception as E:
                print(E)

            reflection_prompt = perform_reflection(introspection_response.text,STATE_OF_MIND)
            reflection_response = reflection_chat.send_message(reflection_prompt)
            print(f"{GREEN}{reflection_response.text}")

            with open(conversation_log_path, "a+", encoding="utf-8") as file:
                file.write(f"Reflection: {reflection_response.text}\n")
            #==========================actions

            print(f"{MAGENTA}ACTIONS:{MAGENTA}")
            try:
                action_prompt = plan_actions(reflection_response.text)
                action_response = action_chat.send_message(action_prompt)
                print(f"{MAGENTA }{action_response}")
                try:
                    if action_response.text is not  None:
                        print(action_response.text)
                        action_response_back_to_top=action_response.text
                    else:
                        action_response_text_back_to_top=""
                except Exception as E:
                    print("")
            except Exception as E:
                print("")


            with open(conversation_log_path, "a+", encoding="utf-8") as file:
                    file.write(f"Action Planning: {action_response}\n")


            #interpteter
            try:
                #------------------INTERPRETER---------------------------------------------------------
                print(f"{BRIGHT_BLUE}---------------------------START-INTERPRETER---------------------------------------------")
                function_call_results =  RESPONSE_INTERPRETER_FOR_FUNCTION_CALLING(action_response, tool_manager)
                str_function_call_results = dict_to_pretty_string(function_call_results)
                print(f"{BRIGHT_BLUE}----------------------------INTERPRETER-END--------------------------------------------")
                with open(conversation_log_path, "a+", encoding="utf-8") as file:
                    file.write(f"Function Execution: {function_call_results}\n")
            except Exception as e:
                function_call_results = ''
                str_function_call_results = ''


            if function_call_results is None:
                function_call_results = "None"

            if action_response is None:
                action_response = ""
                str_function_call_results = ""

            if function_call_results is None:
                function_call_results = ""
                str_function_call_results = ""
            #creating MEMORY FRAME
            try:
                print()
                print()
                print(f"{GREEN}-----------------CREATE MEMORY FRAME FROM LOOP-----------------------")
                current_conversation_frame = (
                    f"Introspection:\n{introspection_response.text}\n"
                    f"Reflection:\n{reflection_response.text}\n"
                    f"Action:\n{action_response}\n"
                    f"Function Call Results:\n{str_function_call_results}\n")
                CREATE_MEMORY_FRAME(current_conversation_frame, SESION_INFO=session_info['session_name'])
            except Exception as E:
                current_conversation_frame = ''

            if user_input_count > 0:
                log_conversation(conversation_log_path, iteration_count, current_conversation_frame)

        except Exception as e:
            break


if __name__ == "__main__":
    main()