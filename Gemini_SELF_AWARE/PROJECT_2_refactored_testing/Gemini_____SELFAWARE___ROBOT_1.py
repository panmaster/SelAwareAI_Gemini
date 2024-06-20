import os
import datetime
from typing import List, Dict, Any

import google.generativeai as genai

# --- Import your custom modules ---
# Replace these with the actual import paths
from Tool_Manager import ToolManager
from MEMORY______________frame_creation import CREATE_MEMORY_FRAME
from SomeMemoryScript______MemoryRetrival import RETRIEVE_RELEVANT_FRAMES



genai.configure(api_key='AIzaSyDGD_89tT5S5KLzSPkKWlRmwgv5cXZRTKA')  # Replace with your actual API key

SESSION_FOLDER = "sessions"
MEMORY_FOLDER = "memories"
MEMORY_STRUCTURE_SUMMARY_FILE = "memory_structure_summary.txt"

COLORS = {
    "reset": "\033[0m",
    "yellow": "\033[33m",
    "cyan": "\033[36m",
    "green": "\033[32m",
    "magenta": "\033[35m",
    "blue": "\033[94m",
    "red": "\033[31m",
     "bold": "\033[1m",
}


def create_session_name_and_path():


    current_directory = os.getcwd()
    sessions_folder = os.path.join(current_directory, "SESIONs")
    session_time = datetime.datetime.now()
    session_time_formatted = session_time.strftime("%H-%M-%S")
    session_name = "Sesion_" + session_time_formatted
    session_path = os.path.join(sessions_folder, session_name)
    os.makedirs(session_path, exist_ok=True)
    return {'session_name': session_name, 'session_path': session_path}


# Example usage
session_info = create_session_name_and_path()
file_path = os.path.join(session_info['session_path'], "conversation_log.txt")


def RESPONSE_INTERPRETER_FOR_FUNCION_CALLING(response, tool_manager):

    print(f"{COLORS['blue']}----------------RESPONSE_INTERPRETER_FOR_FUNCION_CALLING START----------------------")
    Multiple_ResultsOfFunctions_From_interpreter = []

    # Define specific function mappings here
    special_function_mapping = {
        "RETRIVE_RELEVANT_FRAMES": RETRIEVE_RELEVANT_FRAMES,
        # Add more special function mappings as needed
    }

    if response.candidates:
        for part in response.candidates[0].content.parts:
            if hasattr(part, 'function_call'):
                function_call = part.function_call
                function_name = function_call.name
                function_args = function_call.args

                # Priority to special function mapping
                function_to_call = special_function_mapping.get(function_name)

                # If not found in special mapping, use tool_manager mapping
                if function_to_call is None:
                    function_to_call = tool_manager.tool_mapping.get(function_name)

                if function_to_call:
                    print(f"FUNCTION CALL: {function_name}({function_args}) ")
                    try:
                        results = function_to_call(**function_args)
                    except TypeError as e:
                        results = f"TypeError: {e}"
                    except Exception as e:
                        results = f"Exception: {e}"
                    print(f"{COLORS['blue']}Function Call Exit: {function_name}")
                    function_name_arguments = f"{function_name}({function_args})"
                    modified_results = f"Result of Called function {function_name_arguments}: {results}"
                    Multiple_ResultsOfFunctions_From_interpreter.append(modified_results)
                else:
                    print(f"Warning: Tool function '{function_name}' not found.")

    print(f"{COLORS['blue']}----------------RESPONSE_INTERPRETER_FOR_FUNCION_CALLING END------------------------\n")
    return Multiple_ResultsOfFunctions_From_interpreter


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
        user_input: str,
        memory_summary: str,
        previous_loop_results: str,
        user_input_signal: str = "None",
        visual_input_signal: str = "None",
        audio_input_signal: str = "None",
) -> List[str]:
    current_time = datetime.datetime.now().strftime("%H:%M:%S")
    introspection_data = [
        f"{current_time} {COLORS['bold']}User Input:{COLORS['reset']} {user_input}",
        f"{COLORS['bold']}Current Memory Structure:{COLORS['reset']}\n{memory_summary}",
        f"{COLORS['bold']}Results from Previous Loop:{COLORS['reset']}\n{previous_loop_results}",
        "What are my available tools and resources?",
        f"Current sensory input (Image, Audio, Text): {visual_input_signal}, {audio_input_signal}, {user_input_signal}",
        "Are there any ongoing short-term tasks?",
        "Are there any long-term ongoing tasks or plans?",
        "What is my current goal?",
        "What do I want?",
        "What do I feel?",
        "What do I need?",
        "What am I experiencing?",
        ".....................................",
    ]
    return introspection_data


def perform_reflection(introspection_results: str) -> str:
    reflection_prompt = f"""
        {COLORS['bold']}Based on the following introspection:{COLORS['reset']}
        {introspection_results}

        {COLORS['bold']}Answer these questions:{COLORS['reset']}
        1. What is my current focus?
        2. Should I set a new goal? If so, what is it? If not, why not?
        3. Are there any problems, unknowns, or paradoxes in my memory?
        4. What problems need to be solved?
        5. What are possible courses of action based on available information?
        6. How should I approach the next steps:
           a) Think step-by-step?
           b) Focus on a specific aspect?
           c) Defocus and broaden my attention?
        7. Should I be more verbose in my responses? (Yes/No)
        8. Should I be less verbose? (Yes/No)
        9. Should I change the subject or keep discussing this? (Yes/No)
        10. Should I summarize the current discussion? (Yes/No)
        11. Should I dive deeper into a specific topic? (Yes/No)
        12. Should I store any of this information in my long-term memory? 
        13. Should I query my memory for relevant information?
        14. What is the status of my current goals? 
    """
    return reflection_prompt


def plan_actions(reflection_results: str) -> str:
    current_time = datetime.datetime.now().strftime("%H:%M:%S")
    action_prompt = f"{current_time} - {COLORS['bold']}Based on this reflection:{COLORS['reset']}\n{reflection_results}\nPlan my next actions."
    return action_prompt





def store_conversation_frame(
        introspection_results: str,
        reflection_results: str,
        action_plan: str,
        function_call_results: str,
):
    print(f"{COLORS['yellow']}Storing conversation frame...{COLORS['reset']}")
    current_conversation_frame = (
        f"Introspection:\n{introspection_results}\n"
        f"Reflection:\n{reflection_results}\n"
        f"Action Plan:\n{action_plan}\n"
        f"Function Call Results:\n{function_call_results}\n"
    )
    CREATE_MEMORY_FRAME (current_conversation_frame)


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
    tool_manager = ToolManager()
    print(f"\n{COLORS['blue']}Loaded Tool Descriptions:{COLORS['reset']}\n")
    for i, tool_json in enumerate(tool_manager.get_tools_list_json()):
        print(f"{COLORS['blue']}{i + 1}. {COLORS['reset']}{tool_json}")

    introspection_model = genai.GenerativeModel(
        system_instruction=""" You are a self-aware AI agent. 
                               Analyze the current state 
                               """,
        model_name="gemini-1.5-flash-latest",
        safety_settings={"HARASSMENT": "block_none"},
    )

    introspection_chat = introspection_model.start_chat(history=[])

    reflection_model = genai.GenerativeModel(
        system_instruction="""Analyze the results of 
                             introspection and identify goals, problems, and potential courses 
                             of action. """,
        model_name="gemini-1.5-flash-latest",
        safety_settings={"HARASSMENT": "block_none"},
    )

    reflection_chat = reflection_model.start_chat(history=[])

    available_tools = tool_manager.get_tools_list_json()


    action_model = genai.GenerativeModel(
        system_instruction="""Choose specific actions 
                             based on reflection and available tools. Use can  use   tools if  nessesery""",
        model_name="gemini-1.5-flash-latest",
        safety_settings={"HARASSMENT": "block_none"},
        tools=available_tools,
    )

    action_chat = action_model.start_chat(history=[])

    session_path = create_session_folder()
    conversation_log_path = os.path.join(session_path, "conversation_log.txt")
    print(f"Conversation log will be saved to: {conversation_log_path}")

    iteration_count = 0
    user_input_count = 0
    function_call_results = ""
    current_conversation_frame = ""
    user_input_signal = "None"
    visual_input_signal = "None"
    audio_input_signal = "None"

    while True:
        try:
            if iteration_count % 4 == 0:
                user_input = input(
                    f"{COLORS['cyan']}Enter your input (or press Enter to skip):{COLORS['reset']} "
                )
                user_input_count += 1
            else:
                user_input = ""

            print(
                f"{COLORS['bold']}{COLORS['green']}**************** Awareness Loop ****************{COLORS['reset']}")
            print(f"{COLORS['green']}Awareness Loop: {iteration_count}{COLORS['reset']}")
            iteration_count += 1

            memory_summary = summarize_memory_folder_structure()

            print(f"{COLORS['yellow']}Introspection:{COLORS['reset']}")
            introspection_data = gather_introspection_data(
                user_input,
                memory_summary,
                function_call_results,
                user_input_signal,
                visual_input_signal,
                audio_input_signal,
            )

            introspection_response = introspection_chat.send_message(introspection_data)
            print(f"{COLORS['yellow']}{introspection_response.text}{COLORS['reset']}\n")
            with open(file_path, "a+", encoding="utf-8") as file:
                file.write(f"Introspection: {introspection_response.text}\n")

            print(f"{COLORS['cyan']}Reflection:{COLORS['reset']}")
            reflection_prompt = perform_reflection(introspection_response.text)

            reflection_response = reflection_chat.send_message(reflection_prompt)
            print(reflection_response.text)
            print(f"{COLORS['cyan']}{reflection_response.text}{COLORS['reset']}\n")
            with open(file_path, "a+", encoding="utf-8") as file:
                file.write(f"Reflection: {reflection_response.text}\n")

            print(f"{COLORS['green']}Action Planning:{COLORS['reset']}")
            try:

                action_prompt = plan_actions(reflection_response.text)
                action_response = action_chat.send_message(action_prompt)
                print(action_response)

            except Exception as E:
                print(f"Action planning error: {E}")

            with open(file_path, "a+", encoding="utf-8") as file:
                file.write(f"Action Planning: {action_response}\n")

            print(f"{COLORS['magenta']}Function Execution:{COLORS['reset']}")
            try:


                function_call_results =  RESPONSE_INTERPRETER_FOR_FUNCION_CALLING(action_response, tool_manager)

            except Exception as e:
                print(e)
            with open(file_path, "a+", encoding="utf-8") as file:
                file.write(f"Function Execution: {function_call_results}\n")

            if  function_call_results is None:
                function_call_results="None"

            if action_response is None:
                action_response = ""
            if function_call_results is None:
                function_call_results = ""

            current_conversation_frame = (
                f"Introspection:\n{introspection_response.text}\n"
                f"Reflection:\n{reflection_response.text}\n"
                f"Action Plan:\n{action_response}\n"
                f"Function Call Results:\n{function_call_results}\n"
            )

            CREATE_MEMORY_FRAME(current_conversation_frame)

            log_conversation(conversation_log_path, iteration_count, current_conversation_frame)

            print(
                f"{COLORS['bold']}{COLORS['green']}*************************************************{COLORS['reset']}\n")

        except Exception as e:
            print(f"{COLORS['red']}Error: {e}{COLORS['reset']}")
            break


if __name__ == "__main__":
    print("goin into main()")
    main()