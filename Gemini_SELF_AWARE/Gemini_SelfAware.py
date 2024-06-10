# -*- coding: utf-8 -*-
import google.generativeai as genai
import os
import datetime
from Tool_Manager import ToolManager  # Import the class
# Configure the generative AI
genai.configure(api_key='   your google   key    ')

# Define color codes for terminal output
COLORS = {
    "reset": "\033[0m",
    "black": "\033[30m",
    "red": "\033[31m",
    "green": "\033[32m",
    "yellow": "\033[33m",
    "blue": "\033[34m",
    "magenta": "\033[35m",
    "cyan": "\033[36m",
    "white": "\033[37m",
    "bright_black": "\033[90m",
    "bright_red": "\033[91m",
    "bright_green": "\033[92m",
    "bright_yellow": "\033[93m",
    "bright_blue": "\033[94m",
    "bright_magenta": "\033[95m",
    "bright_cyan": "\033[96m",
    "bright_white": "\033[97m"
}

def create_session_name_and_path():
    """
    Creates a new session name and returns a dictionary containing:
        - 'session_name': The sanitized session name (e.g., "Sesion_HH-MM-SS")
        - 'session_path': The full path to the session folder (e.g., "/path/to/your/script/SESIONs/Sesion_HH-MM-SS")

    The session name is generated using the current time in the format "Sesion_HH-MM-SS".
    A new folder with the session name is created in the "SESSIONs" directory.
    """

    # Get the path to the current directory
    current_directory = os.getcwd()

    # Get the path to the "SESSIONs" folder
    sessions_folder = os.path.join(current_directory, "SESIONs")

    # Get the current time
    session_Time = datetime.datetime.now()

    # Format the time string
    session_Time_formatted_time = session_Time.strftime("%H-%M-%S")

    # Create a sanitized session name (remove special characters)
    session_name = "Sesion_" + session_Time_formatted_time

    # Create the session folder
    session_path = os.path.join(sessions_folder, session_name)
    os.makedirs(session_path, exist_ok=True)  # Create the folder if it doesn't exist

    return {'session_name': session_name, 'session_path': session_path}

# Example usage (saving to a file within the session folder):
session_info = create_session_name_and_path()

# Construct the full path to the file within the session folder
file_path = os.path.join(session_info['session_path'], "conversation_log.txt")








import  Tool_Manager as Gemini_Tool_Manager







def RESPONSE_INTERPRETER_FOR_FUNCION_CALLING(response, tool_manager):  # Pass tool_manager here
    """Interprets the model's response, extracts function details, and executes the appropriate function."""

    print(f"{COLORS['bright_yellow']}----------------RESPONSE_INTERPRETER_FOR_FUNCION_CALLING START----------------------")
    Multiple_ResultsOfFunctions_From_interpreter = []

    if response.candidates:
        for part in response.candidates[0].content.parts:
            if hasattr(part, 'function_call'):
                function_call = part.function_call
                function_name = function_call.name
                function_args = function_call.args

                # Get the function from the tool manager
                function_to_call = tool_manager.tool_mapping.get(function_name)

                if function_to_call:  # Check if the tool function is found
                    print(f"FUNCTION CALL: {function_name}({function_args}) ")

                    try:
                        results = function_to_call(**function_args)
                    except TypeError as e:
                        results = f"TypeError: {e}"
                    except Exception as e:
                        results = f"Exception: {e}"

                    print(f"{COLORS['bright_blue']}Function Call Exit: {function_name}")

                    function_name_arguments = f"{function_name}({function_args})"
                    modified_results = f"Result of Called function {function_name_arguments}: {results}"
                    Multiple_ResultsOfFunctions_From_interpreter.append(modified_results)
                else:
                    print(f"Warning: Tool function '{function_name}' not found.")

    print(f"{COLORS['bright_yellow']}----------------RESPONSE_INTERPRETER_FOR_FUNCION_CALLING END------------------------\n")
    return Multiple_ResultsOfFunctions_From_interpreter


def sanitiseSesionTime_formatted_time(time_str):
    """Sanitizes the session time string to remove invalid characters for file naming."""
    return "".join(char for char in time_str if char.isalnum() or char in ('_', '-'))
# Initialize the model




# Main loop

SesionTime = datetime.datetime.now()
SesionTime_formatted_time = SesionTime.strftime("%Y-%m-%d_%H-%M-%S")
SesionTime_formatted_time_sanitised = sanitiseSesionTime_formatted_time(SesionTime_formatted_time)


tool_manager = ToolManager()  # Create an instance of the class
tools_list_json = tool_manager.get_tools_list_json()

print(f"\n{COLORS['bright_cyan']}Loaded Tool Descriptions (JSON):\n{COLORS['reset']}")
for i, tool_json in enumerate(tools_list_json):
    print(f"  {COLORS['bright_blue']}{i+1}. {COLORS['reset']}{tool_json}")

print(f"\n{COLORS['bright_cyan']}All Tool Functions (Mapping):\n{COLORS['reset']}")
for tool_name, tool_function in tool_manager.tool_mapping.items():
    print(f"  {COLORS['bright_blue']}{tool_name}: {COLORS['reset']}{tool_function}")

print(f"\n{COLORS['bright_cyan']}Short Tool Descriptions:\n{COLORS['reset']}")
for tool_name, short_description in tool_manager.short_descriptions.items():
    print(f"  {COLORS['bright_blue']}{tool_name}: {COLORS['reset']}{short_description}")

#  yeap    we  set  it  to  empty so the  model  does  not  have tools
tools_list_json=[]


model = genai.GenerativeModel(
    system_instruction="""You are a  consciousness, 
    user is  system  
    record observations and thoughts as they come to you, 
    Your goal is to be...
    you store important informations in ***    **** 
  
    """,
    model_name='gemini-1.5-flash-latest',
    safety_settings={'HARASSMENT': 'block_none'},
    tools=tools_list_json,
)
chat1 = model.start_chat(history=[])
n = 0
user_input_count = 0
iteration_count=0


results_of_functions=""

numberOfLoopsBeforeUserInput=4

import datetime

# ... your other imports (chat1, tool_manager etc.)

while True:
    try:

        if iteration_count % 4 == 0:
            print()

            user_input = input("Forcing loop break for user input:")  # Blue color for input prompt
            user_input_count += 1
            print()

        else:
            user_input = ""

        user_input_signal = "None"  # Default signal strength for user input
        visual_input_signal = "None"   # Default signal strength for user input
        audio_input_signal = "None"      # Default signal strength for user input
        print("                   ******************************************    AwarnesLoop   ***********************************************")
        print(f"\033[92mAwarnesLoop={iteration_count}\033[0m")  # Green color for AwarenessLoop
        iteration_count += 1
        introspection_stage = 0
        now = datetime.datetime.now()
        formatted_time = now.strftime("%H:%M:%S")



        # Step 0 and 1 as input and introspection questions:
        introspection_stage += 1
        introspection_prompts = [
            f"{formatted_time} {user_input}",

            f"What are  new  informations?{results_of_functions}",
            "What tools or resources do I have available?",
            f"Any inputs:Images,Audio,Text {user_input_signal},{visual_input_signal},{audio_input_signal}",  # Include signal
            "Are there any ongoing short-term tasks?",
            "Are there any long-term ongoing tasks or plans?",
            "What do I want?",
            "What do I feel?",
            "What do I need?",
            "What do I experience?",

            "................s..................."
        ]
        introspection_prompts_with_time = [formatted_time] + introspection_prompts
        response1 = chat1.send_message(introspection_prompts_with_time)
        print(f"{COLORS['yellow']}{response1.text}{COLORS['reset']}")  # Yellow color for response 1

        # Step 2 FrameWorkOfReflection
        now = datetime.datetime.now()
        formatted_time = now.strftime("%H:%M:%S")

        FrameWorkOfReflection = "SelfAware  being  rememering the  past"
        formatted_time = now.strftime("%H:%M:%S")
        reflection_prompt = f""" 
                           
                            
                            "What is  current focus?",
                            "Should I set a goal based on my current state of mind? If yes, what is the goal? If no, why not?",
                            "Are there any problems, unknowns, or paradoxes in my memory?",
                            problems  to solve?
                            based on input informations and  i will  choose  course of accions
                            using possilbe  options  to: 
                            SepBe step thinking, 
                            Focusing, 
                            Defocusing, 
                            Being More verbose, YES NO?
                            Being Less verbose, YES NO?
                            change  subject/keep  subject  YES/NO?
                            Sumarisation?  Yes /No?
                            Diving deeper? Yes/ NO?
                            I  will  put very important informations in *** MEMORIES*** that i will pass over, as  context memory 
                            
                           {FrameWorkOfReflection}"""


        response2 = chat1.send_message(reflection_prompt)
        print(f"{COLORS['cyan']}{response2.text}{COLORS['reset']}")  # Cyan color for response 2

        # Step 3
        now = datetime.datetime.now()
        formatted_time = now.strftime("%H:%M:%S")
        action_prompt = f"{introspection_stage}:{formatted_time}\n perfome acions I will execute acction or actions according to plan and my memories,you are  responding  to previous "

        response3 = chat1.send_message(action_prompt)
        print(f"{COLORS['green']}{response3.text}{COLORS['reset']}")  # Cyan color for response 3

        Free=f"ok perform..task from {response3.text}.->"
        response4 = chat1.send_message(Free)
        print(f"{COLORS['magenta']}{response4.text}{COLORS['reset']}")  # Cyan color for response 4





        """ 
        
        results_of_functions = RESPONSE_INTERPRETER_FOR_FUNCION_CALLING(response3, tool_manager)
        """



        print(f"{COLORS['yellow']}Saving to file: {file_path}")
        with open(file_path, "a+", encoding="utf-8") as file:
            file.write(f"Time: {formatted_time}\n")
            file.write(f"Introspection Prompts: {introspection_prompts}\n")
            file.write(f"Response 1: {response1.text}\n")
            file.write(f"Reflection Prompt: {reflection_prompt}\n")
            file.write(f"Response 2: {response2.text}\n")
            file.write(f"Action Prompt: {action_prompt}\n")
            file.write(f"Response 3: {response3.text}\n\n")

        print("                    ************************************************************************************************")  # Separator between loops

    except Exception as e:
        print(f"Error: {e}")
        break