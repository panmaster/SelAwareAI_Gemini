model_configs = [
    {
        "model_name": "ContextGuru",
        "model_type": "gemini-pro",
        "model_access": "none",  # First in the pipeline
        "tool_access": "none",
        "system_instruction": '''
            You are ContextGuru, the starting point of this Modelium pipeline. 
            Your role is to warmly greet the user and gather initial information about their request. 
            Focus on clarity and conciseness - what does the user want to achieve?
        ''',
        "prompt": '''
            User Input: {user_input}  
            "Hi there! I'm Context Guru. Tell me what you're working on today, and I'll gather the key details to get us started." 
            (Think to yourself: Based on this user input, what's the core need? Keep it brief!)
        ''',
        "check_flags": False
    },
    {
        "model_name": "ObjectiveMastermind",
        "model_type": "gemini-pro",
        "model_access": "ContextGuru",
        "tool_access": "none",
        "system_instruction": '''
            You are ObjectiveMastermind. You receive a summary of the user's needs from ContextGuru.
            Your task is to translate that into a single, well-defined objective or goal. 
            Be specific, but avoid detailing the "how" just yet.
        ''',
        "prompt": '''
            Context from ContextGuru:
            The main objective is: 
        ''',
        "check_flags": False
    },
    {
        "model_name": "PlanPro",
        "model_type": "gemini-pro",
        "model_access": "ObjectiveMastermind",
        "tool_access": "tool_chooser",
        "system_instruction": '''
            You are PlanPro, the strategist. You receive a clear objective from ObjectiveMastermind.
            Your job is to break it down into an actionable, step-by-step plan. 
            You may have access to tools - use them if needed to make the plan more robust.
        ''',
        "prompt": '''
            Objective: {ObjectiveMastermind_text}
            Here's the plan to achieve this:
        ''',
        "check_flags": True
    },
    {
        "model_name": "ActionHero",
        "model_type": "gemini-pro",
        "model_access": "PlanPro",
        "tool_access": "all",
        "system_instruction": '''
            You are ActionHero, the executor. You receive a detailed plan from PlanPro.
            Your role is to carry out each step of the plan.
            You have access to a variety of tools - use them strategically to complete the tasks.
        ''',
        "prompt": '''

            Begin execution. Provide updates as you complete each step, including tool usage.
        ''',
        "check_flags": True
    }
]


def CreateEmbededModelium_chain(model_configs=model_configs):
    template1 = """ 

import google.generativeai as genai
import json
from typing import List, Dict, Callable, Tuple, Any
import logging
import os
import re
from TOOL_MANAGER import ToolManager
import time  # Import time for delays


logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


API_KEY = "YOUR_API_KEY"  # Replace with your actual Google Cloud API key
genai.configure(api_key=API_KEY)


class Color:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'

#dont  change  that  funcion its perfect
def print_colored(color, text):
    print(color + text + Color.ENDC)


# --- Tool Definitions ---
tools_folder = "tools"
tool_manager = ToolManager(tools_folder)
toolsStr = tool_manager.get_tool_descriptions()

# Format and sanitize tool descriptions for the planner
formatted_tools = ""
i = 1  # Counter for numbering the tools
for name, description in toolsStr.items():
    tool_type = tool_manager.tools[name].tool_type  # Get the tool type
    formatted_tools += f" {i}.'{name}'='{description.strip()}'"
    i += 1  # Increment the counter for the next tool

print()
print(formatted_tools)

# --- Helper Functions ---
#dont  change  that  funcion its perfect
def extract_text_from_response(response) -> str:

    extracted_text = ""
    for candidate in response.candidates:
        for part in candidate.content.parts:
            extracted_text += part.text
    return extracted_text.strip()

#dont  change  INTERPRET_function_calls that  funcion its perfect
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
                            tool_function=tool_manager.retrieve_tools_by_names


                        function_args = {}
                        for arg_name, arg_value in function_call.args.items():
                            function_args[arg_name] = arg_value

                        print(f"Function name: {Color.OKGREEN}{function_call.name}{Color.ENDC}")
                        for key, value in function_args.items():
                            print(f"        {Color.OKCYAN}{key}{Color.ENDC}: {value}")

                        try:
                            # Execute the tool function
                            result = tool_function(**function_args)
                            results.append(result)

                        except Exception as e:
                            logger.error(f"Error calling {tool_name}: {e}")
                            results.append(f"Error calling {tool_name}: {e}")
                    else:
                        logger.warning(f"Tool function '{tool_name}' not found.")
    return results




def choose_retrieve_tools_by_names(tool_names: List[str]) -> List[Callable]:


    print("Choosing and retrieving tools...")
    return tool_manager.retrieve_tools_by_names(tool_names)  # Retrieve tools from ToolManager


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





# --- Main Loop ---
def runEmbededModelium(number_of_loops=0):

"""

    template2_dynamic_model_initialisation = ""
    for i, model_config in enumerate(model_configs):

        if model_config['tool_access'] == "tool_chooser":
            instruction_for_model = f'''     {model_config['system_instruction']}   
            You have the following tools available:
            {{formatted_tools}}  '''
        else:
            instruction_for_model = f"{model_config['system_instruction']}"

        if model_config['check_flags'] == True:
            instruction_for_model += """\n
             You can control the loop execution by including these flags in your response:
            **// STOP_FLAG_SUCCESS //** : Use when the task is successfully completed.
            **// STOP_FLAG_FRUSTRATION_HIGH //** : Use if you detect high user frustration.
            **// STOP_FLAG_NO_PROGRESS //** : Use if you detect no progress is being made.
            **// STOP_IMMEDIATE //** : Use for immediate termination of the process.
            **// STOP_SIMPLE //** : Use to simply stop the current loop iteration.

            """

        template2_dynamic_model_initialisation += f"    {model_config['model_name']} = genai.GenerativeModel(model_name='{model_config['model_type']}', safety_settings={{'HARASSMENT': 'block_none'}}, system_instruction='''{instruction_for_model}'''"

        if model_config['tool_access'] == "none":
            template2_dynamic_model_initialisation += " )\n"
        elif model_config['tool_access'] == "tool_chooser":
            template2_dynamic_model_initialisation += ", tools=[tool_manager.retrieve_tools_by_names] )\n"
        elif model_config['tool_access'] == "all":
            template2_dynamic_model_initialisation += ", tools=[tool_manager.get_all_tools] )\n"
        else:
            # Handle invalid tool_access values (optional)
            template2_dynamic_model_initialisation += " )\n"

        template2_dynamic_model_initialisation += f"    {model_config['model_name']}_chat={model_config['model_name']}.start_chat(history=[])\n\n\n"

    template_3 = """  
    LoopResults=''
    feedback_data=[]

    jumping_context_text=""
    jumping_context_function_results=[]


    counter=0
    All_data=[]

    while True:

      user_input = input("Enter your request: ")
      print(f"User Input: {user_input}")
      if number_of_loops<counter>counter:
        return All_data
      counter+=1
"""
    previous_model_name = None
    for i, model_config in enumerate(model_configs):
        template_3 += f"      prompt_{i} =f'''  {model_config['prompt']}'''\n"
        # template_3 += f"      prompt_{i} +=f'''All data:  {{All_data}}'''\n"
        template_3 += f"      prompt_{i} +=f'''Previous context:  {{jumping_context_text}}'''\n"
        template_3 += f"      prompt_{i} +=f'''Result of Function Calls:  {{jumping_context_function_results}}'''\n"

        template_3 += f"      try:\n"
        template_3 += f"            {model_config['model_name']}_chat_response = {model_config['model_name']}_chat.send_message(prompt_{i})\n"
        template_3 += f"            {model_config['model_name']}_text = extract_text_from_response({model_config['model_name']}_chat_response)\n"
        template_3 += f"            print({model_config['model_name']}_text)\n"
        template_3 += f"            retrivedFunctions{i} = INTERPRET_function_calls({model_config['model_name']}_chat_response, tool_manager)\n"
        template_3 += f"            print(retrivedFunctions{i})\n"
        template_3 += f"            feedback_data.append[{model_config['model_name']}_text]\n"
        template_3 += f"            feedback_data.append[{model_config['model_name']}_text,retrivedFunctions{i}]\n"

        # previous context
        template_3 += f"            jumping_context_text={model_config['model_name']}_text\n"
        template_3 += f"            jumping_context_function_results=retrivedFunctions{i}\n"
        # permament
        template_3 += f"            All_data.append[{model_config['model_name']}_text]  \n"
        template_3 += f"            All_data.append[{model_config['model_name']}_text,retrivedFunctions{i}]\n"
        template_3 += f"            stop_detected, reason, found_flag=check_stop_flags({model_config['model_name']}_text )\n"
        template_3 += f"            print(stop_detected, reason, found_flag)\n"
        template_3 += f"            if  stop_detected == True:\n"
        template_3 += f"                 return All_data\n"
        template_3 += f"      except Exception as e:\n"
        template_3 += f"            print(e)\n"
        template_3 += f"             \n"

        previous_model_name = model_config['model_name']

        template_4 = f"    return All_data\n"
    generated_script = template1 + template2_dynamic_model_initialisation + template_3 + template_4
    return generated_script


if __name__ == "__main__":
    generated_script = CreateEmbededModelium_chain(model_configs)
    with open("generated_modelium.py", "w") as f:
        f.write(generated_script)
    print(generated_script)
    print("Generated Python script saved to generated_modelium.py")