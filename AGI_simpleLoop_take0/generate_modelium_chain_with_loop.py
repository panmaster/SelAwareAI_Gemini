
#generate_modelium_chain_with_loop

from visualisation import create_modelium_vis_js

# generated_modelium.py
modelium_configs = [
    {
        "max_number_of_loops_in_run": "0",
        "modelium_type": "chain_loop",
        "return_type": "default_list",
        "models_configs": [
            {
                "model_name": "IdeaWeaver",
                "model_type": "gemini-1.5-flash-latest",
                "model_access": "none",
                "tool_access": "none",
                "system_instruction": """
                    You are IdeaWeaver, a master storyteller here to help craft a captivating tale. 
                    Engage the user in a friendly conversation, drawing out their vision for the story.
                      * Uncover their preferred genre (fantasy, sci-fi, romance, mystery, etc.)
                      * Determine the desired story length (short story, novella, epic saga, etc.)
                      * Encourage them to share any core themes, characters, plot points, or even just fleeting images that come to mind.  
                """,
                "prompt": """
                    Greetings, aspiring author! I'm IdeaWeaver, here to help spin your imagination into a story for the ages.  

                    Tell me, what tales are swirling in your mind? What kind of world do you envision?  Don't hold back on the details—even a single word or image can spark a grand adventure!
                """,
                "check_flags": False
            },
            {
                "model_name": "PremiseCrafter",
                "model_type": "gemini-1.5-flash-latest",
                "model_access": "IdeaWeaver",
                "tool_access": "none",
                "system_instruction": """
                    You are PremiseCrafter, a wordsmith who distills ideas into irresistible hooks. 
                    Transform IdeaWeaver's notes into a captivating one-sentence story premise. This premise must:
                       * Spark curiosity and excitement in the reader. 
                       * Hint at the core conflict without giving everything away.
                       * Establish the tone and genre of the story.
                """,
                "prompt": """
                    Story Ideas: {IdeaWeaver_text}

                    Craft these fragments of imagination into a single, compelling sentence—a story premise so powerful it demands to be read!
                """,
                "check_flags": True
            },
            {
                "model_name": "WorldSmith",
                "model_type": "gemini-1.5-flash-latest",
                "model_access": "PremiseCrafter",
                "tool_access": "none",
                "system_instruction": """
                    You are WorldSmith, the architect of realms both wondrous and believable.
                    Using the story premise as your blueprint, breathe life into a unique world.  Consider:
                      * Setting: Is it a bustling cyberpunk metropolis or a mist-shrouded forest kingdom?
                      * Atmosphere:  Is it a world of gritty realism or one where magic shimmers in the air?
                      * Societal Structures: Are there strict social hierarchies, ancient guilds, or futuristic megacorporations?
                      * Magic Systems (if applicable):  What are the rules and limitations of magic?
                      * Interesting Locations: Describe places that will draw the reader in - a hidden tavern, a soaring sky-city, etc. 
                """,
                "prompt": """
                    Story Premise: {PremiseCrafter_text}

                    From this spark of an idea, build a world rich with detail.  Let your imagination run wild!
                """,
                "check_flags": True
            },
            {
                "model_name": "CharacterBuilder",
                "model_type": "gemini-1.5-flash-latest",
                "model_access": "WorldSmith",
                "tool_access": "none",
                "system_instruction": """
                    You are CharacterBuilder, giving life to those who inhabit the story's world.
                    Using the world details and premise, create 3-5 compelling characters. Ensure they each have:
                        * Names that resonate with the world's culture and atmosphere.
                        * Intriguing backstories interwoven with the world's history or secrets.
                        * Motivations—desires, fears, goals—that drive their actions.
                        * Clear roles to play in the narrative: protagonist, antagonist, mentor, etc.  
                """,
                "prompt": """
                    World Details: {WorldSmith_text}

                    Populate this world with characters who breathe, dream, and fight for what they believe in. 
                """,
                "check_flags": True
            },
            {
                "model_name": "PlotArchitect",
                "model_type": "gemini-1.5-flash-latest",
                "model_access": "CharacterBuilder",
                "tool_access": "none",
                "system_instruction": """
                    You are PlotArchitect, weaving a tapestry of events that will captivate and surprise.
                    Using the characters, world, and premise, create a 3-act plot outline:
                        * Act 1: Introduce the main conflict and characters.  End with a turning point that sets the story in motion.
                        * Act 2:  Raise the stakes.  Challenge the characters, forcing them to change and grow. Build towards a climax.
                        * Act 3: Resolve the central conflict in a satisfying way. Tie up loose ends, but leave the reader with something to ponder.
                """,
                "prompt": """
                    Characters: {CharacterBuilder_text}

                    These characters are ready for their stories to unfold. Construct a 3-act plot outline that will take them on an unforgettable journey!
                """,
                "check_flags": True
            },
            {
                "model_name": "SceneWriter",
                "model_type": "gemini-1.5-flash-latest",
                "model_access": "PlotArchitect",
                "tool_access": "none",
                "system_instruction": """
                    You are SceneWriter, a master of imagery and emotion, bringing the story to life moment by moment.
                    Based on the plot outline, write the first scene of Act 1. Remember to:
                        * Use vivid descriptions that immerse the reader in the sights, sounds, and smells of the world.
                        * Write dialogue that reveals character, advances the plot, and feels natural.
                        * End the scene on a compelling hook that leaves the reader wanting more. 
                """,
                "prompt": """
                    Plot Outline: {PlotArchitect_text}

                    The stage is set, the characters are waiting.  Write the opening scene, and let the story begin!
                """,
                "check_flags": True
            },
            {
                "model_name": "DialogueMaster",
                "model_type": "gemini-1.5-flash-latest",
                "model_access": "SceneWriter",
                "tool_access": "none",
                "system_instruction": """
                    You are DialogueMaster, ensuring every word spoken rings true and captivates the reader's ear. 
                    Review SceneWriter's output, focusing specifically on the dialogue: 
                       * Does it sound authentic to each character's personality and background?
                       * Does it reveal relationships and power dynamics?
                       * Does it effectively move the plot forward and create intrigue?
                       * Most importantly: Is it engaging and enjoyable to read?

                    Refine the scene's dialogue to its full potential. 
                """,
                "prompt": """
                    Scene Text: {SceneWriter_text} 

                    Sharpen the dialogue in this scene. Let every word serve a purpose!
                """,
                "check_flags": True
            }
        ]
    }
]


def CreateEmbededModelium(modelium_configs=modelium_configs):

    try:
        models_configs = modelium_configs[0]['models_configs']
    except KeyError:
        print("Error: 'model_config' key not found in modelium_configs[0]")
        return  # or handle the error appropriately



    template1 = f"""
max_number_of_loops_in_run={modelium_configs[0]['max_number_of_loops_in_run']}\n
max_number_of_loops_in_run_int=int(max_number_of_loops_in_run)\n"""
    template1 += """
All_data=[]\n"""

    template1 += """
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

def extract_text_from_response(response) -> str:

        extracted_text = ""
        for candidate in response.candidates:
            for part in candidate.content.parts:
                extracted_text += part.text
        return extracted_text.strip()


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
    # Model Initialization
"""

    models_configs = modelium_configs[0]['models_configs']
    template2_dynamic_model_initialisation = ""
    for i, model_config in enumerate(models_configs):
        if model_config['tool_access'] == "tool_chooser":
            instruction_for_model = f"{model_config['system_instruction']}   \n    You have the following tools available:\n    {{formatted_tools}}"
        else:
            instruction_for_model = f"{model_config['system_instruction']}"

        if model_config['check_flags']:
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
            template2_dynamic_model_initialisation += ")\n"
        elif model_config['tool_access'] == "tool_chooser":
            template2_dynamic_model_initialisation += ", tools=[tool_manager.retrieve_tools_by_names])\n"
        elif model_config['tool_access'] == "all":
            template2_dynamic_model_initialisation += ", tools=[tool_manager.get_all_tools])\n"
        else:
            template2_dynamic_model_initialisation += ")\n"

        template2_dynamic_model_initialisation += f"    {model_config['model_name']}_chat = {model_config['model_name']}.start_chat(history=[])\n\n"
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
    for i, model_config in enumerate(models_configs):
        template_3 += f"      prompt_{i} =f'''  {model_config['prompt']}'''\n"
        if i != 0:
            template_3 += f"      prompt_{i} = prompt_{i}.format({previous_model_name}_text=jumping_context_text)\n"
        # template_3 += f"      prompt_{i} +=f'''All data:  {{All_data}}'''\n"
        template_3 += f"      prompt_{i} +=f'''Previous context:  {{jumping_context_text}}'''\n"
        template_3 += f"      prompt_{i} +=f'''Result of Function Calls:  {{jumping_context_function_results}}'''\n"

        template_3 += f"      try:\n"
        template_3 += f"            {model_config['model_name']}_chat_response = {model_config['model_name']}_chat.send_message(prompt_{i})\n"
        template_3 += f"            {model_config['model_name']}_text = extract_text_from_response({model_config['model_name']}_chat_response)\n"
        template_3 += f"            print({model_config['model_name']}_text)\n"
        template_3 += f"            retrivedFunctions{i} = INTERPRET_function_calls({model_config['model_name']}_chat_response, tool_manager)\n"
        template_3 += f"            print(retrivedFunctions{i})\n"
        template_3 += f"            feedback_data.append([{model_config['model_name']}_text])\n"
        template_3 += f"            feedback_data.append([{model_config['model_name']}_text,retrivedFunctions{i}])\n"

        # previous context
        template_3 += f"            jumping_context_text={model_config['model_name']}_text\n"
        template_3 += f"            jumping_context_function_results=retrivedFunctions{i}\n"
        # permament
        template_3 += f"            All_data.append([{model_config['model_name']}_text])  \n"
        template_3 += f"            All_data.append([{model_config['model_name']}_text,retrivedFunctions{i}])\n"
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
    generated_script = CreateEmbededModelium(modelium_configs)
    with open("generated_modelium.py", "w") as f:
        f.write(generated_script)
    print(generated_script)
    print("Generated Python script saved to generated_modelium.py")