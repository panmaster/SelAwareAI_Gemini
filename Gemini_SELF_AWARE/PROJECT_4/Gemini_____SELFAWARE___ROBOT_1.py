import os
import datetime
import json
import time

from IPython.display import display, Markdown, clear_output
from rich.console import Console
import google.generativeai as genai
from prettytable import PrettyTable
import json
from MEMORY______________frame_creation import CREATE_MEMORY_FRAME as CREATE_MEMORY_FRAME
from Tool_Manager import ToolManager


genai.configure(api_key='AIzaSyDGD_89tT5S5KLzSPkKWlRmwgv5cXZRTKA')  # Replace with your actual API key

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



def create_session_name_and_path():
    current_directory = os.getcwd()
    sessions_folder = os.path.join(current_directory, "SESIONS")
    session_time = datetime.datetime.now()
    session_time_formatted = session_time.strftime("%H-%M-%S")
    session_name = "Sesion_" + session_time_formatted
    session_path = os.path.join(sessions_folder, session_name)
    os.makedirs(session_path, exist_ok=True)
    return {'session_name': session_name, 'session_path': session_path}


def RESPONSE_INTERPRETER_FOR_FUNCION_CALLING(response, tool_manager):
    """Interprets the response, extracts function details, and executes the function."""

    print(f"{BRIGHT_BLUE}----------------RESPONSE_INTERPRETER_FOR_FUNCION_CALLING START----------------------")
    Multiple_ResultsOfFunctions_From_interpreter = []

    if response.candidates:
        for candidate in response.candidates:
            if hasattr(candidate.content, 'function_call'):
                function_call = candidate.content.function_call
                function_name = function_call.name
                function_args = function_call.args

                function_to_call = tool_manager.tool_mapping.get(function_name)

                if function_to_call:
                    print(f"FUNCTION CALL: {function_name} ")
                    for item in function_args:
                        print(f"argument: {item}")

                    try:
                        # Pass the function_args dictionary directly
                        results = function_to_call(**function_args)
                    except TypeError as e:
                        results = f"TypeError: {e}"
                    except Exception as e:
                        results = f"Exception: {e}"

                    Multiple_ResultsOfFunctions_From_interpreter.append(results)
                else:
                    print(f"Warning: Tool function '{function_name}' not found.")


    if Multiple_ResultsOfFunctions_From_interpreter is not  None:
        for result in  Multiple_ResultsOfFunctions_From_interpreter:
            print(result)
    print(f"{BRIGHT_BLUE}----------------RESPONSE_INTERPRETER_FOR_FUNCION_CALLING END------------------------\n")
    return Multiple_ResultsOfFunctions_From_interpreter



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
        action_response_back_to_top: str ="None",
        user_input: str = "None",
        memory_summary: str = "None",
        previous_loop_results: str = "None",
        user_input_signal: str = "None",
        visual_input_signal: str = "None",
        audio_input_signal: str = "None",
) -> list[str]:
    current_time = datetime.datetime.now().strftime("%H:%M:%S")
    introspection_data = [
        f"Internal memory= {memory_summary}",
        f"{current_time} Past {action_response_back_to_top} current Inputs:  {user_input}",
        f"Past:Function Execution ={previous_loop_results}",
        "What are my available tools and resources?",
        f"Current sensory input (Image, Audio, Text): {visual_input_signal}, {audio_input_signal}, {user_input_signal}",
        "Are there any ongoing short-term tasks?",
        "Are there any long-term ongoing tasks or plans?",

        "1.What is my current goal?",
        "2.What do I want?",
        "3.What am I feeling?",
        "4.What do I need?",
        "5.What am I experiencing?",
        "6 Additional.....",
        "7 Additional.....",
        "8 Emotional state.....",
    ]
    return introspection_data


def perform_reflection(introspection_results: str) -> str:
    current_time = datetime.datetime.now().strftime("%H:%M:%S")
    reflection_prompt = f"""{current_time}

        {introspection_results}
        user is  system, Me is  you
        1. What is  current focus?
        2. Should  set a new goal? If so, what is it? If not, why not?
        3. Are there any problems, unknowns, or paradoxes in my memory?
        4. What problems need to be solved?
        5. What are possible courses of action based on available information?
        6. Approach the next steps?:
           a) Think step-by-step?
           b) Focus on a specific aspect?
           c) Defocus and broaden my attention?
        7. Should I be more verbose in my responses? (Yes/No)
        8. Should I be less verbose? (Yes/No)
        9. Should I change the subject or keep discussing this? (Yes/No)
        10. Should I summarize the current discussion? (Yes/No)
        11. Should I dive deeper into a specific topic? (Yes/No)
        12. Should I store any of this information in my long-term memory (Yes/No)? 
        13. Should I query my memory for relevant information? (Yes/No)
        14. What is the status of my current goals? 
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
    action_response_back_to_top = ""



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
    print("prompt init")
    system_instruction_input= """ 
        user is  assistant and  system in one
        you are answering self questions
        user is system,system is user
        """

    system_instruction_reflection= """ 
        user is  assistant and  system,  
        you answer the questions,
        """

    system_instruction_action = """
         
        you  can Choose specific actions based on reflection and available tools, 
        Use tools if necessary,"""
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

        )


        introspection_chat = introspection_model.start_chat(history=[])
        time.sleep(0.5)
        reflection_model = genai.GenerativeModel(
            system_instruction=system_instruction_reflection,
            model_name="gemini-1.5-flash-latest",
            safety_settings={"HARASSMENT": "block_none"},

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
            if iteration_count % 3 == 0:
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
            print(memory_summary)

            introspection_data = gather_introspection_data(
                action_response_back_to_top,
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
            reflection_prompt = perform_reflection(introspection_response.text)
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
                if action_response.text is not  None:
                    print(action_response.text)
                    action_response_back_to_top=action_response.text
                else:
                    action_response_back_to_top=""


            except Exception as E:
                action_response = ''

            try:
                with open(conversation_log_path, "a+", encoding="utf-8") as file:
                    file.write(f"Action Planning: {action_response}\n")
            except Exception as E:
                action_response = ''

            print(f"{BLUE}Function Execution:{RESET}")
            #interpteter
            try:
                #------------------INTERPRETER---------------------
                function_call_results = RESPONSE_INTERPRETER_FOR_FUNCION_CALLING(action_response, tool_manager)
                str_function_call_results = dict_to_pretty_string(function_call_results)

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

            try:
                print("CREATE MEMORY FRAME FROM LOOP")
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