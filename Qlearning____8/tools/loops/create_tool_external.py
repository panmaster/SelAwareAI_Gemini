tool_type_for_Tool_Manager = "os"

import logging
import google.generativeai as genai
from typing import Dict, List, Any
from dotenv import load_dotenv
import os
import json

# Load environment variables and set up logging
load_dotenv()
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Constants
MODEL_NAME = 'gemini-1.5-flash-latest'
API_KEY = 'AIzaSyBqdQk7ybnS3Mvpr0IhKElcvgv57o6HYnE'  # Replace with your actual API key
genai.configure(api_key=API_KEY)


class AIModel:
    def __init__(self, instruction: str):
        self.model = genai.GenerativeModel(
            system_instruction=instruction,
            model_name=MODEL_NAME,
            safety_settings={"HARASSMENT": "block_none"}
        ).start_chat(history=[])

    def send_message(self, message: str) -> str:
        try:
            response = self.model.send_message(message)
            return self.extract_text_from_response(response)
        except Exception as e:
            logger.error(f"Error sending message to AI model: {e}")
            return ""

    def extract_text_from_response(self, response) -> str:
        try:
            return response.text
        except Exception as e:
            logger.error(f"Error extracting text from Gemini response: {e}")
            return ""


def save_to_file(content: str, filename: str) -> bool:
    """
    Save content to a file.

    content should be trimmed:
      - If ```python is found, then ```python is removed
      - Everything before it is removed
      - At the end of script, find #end
      - Remove #end and everything after it
    """
    path = f"tools/ai_generated_tools/{filename}"
    try:
        content = content.strip()
        if "```python" in content:
            content = content.split("```python")[1]
        if "#end" in content:
            content = content.split("#end")[0].strip()
        # Check for trailing ``` and remove if present
        if content.endswith("```"):
            content = content[:-3].strip()
        with open(path, 'w') as file:
            file.write(content)
        logger.info(f"Successfully saved content to {filename}")
        return True
    except Exception as e:
        logger.error(f"Error saving to file {filename}: {e}")
        return False


def check_files(directory: str = 'tools/ai_generated_tools') -> List[str]:
    """
    Check and return a list of files in the specified directory.
    """
    try:
        files = [f for f in os.listdir(directory) if os.path.isfile(os.path.join(directory, f))]
        logger.info(f"Files in directory {directory}: {files}")
        return files
    except Exception as e:
        logger.error(f"Error checking files in directory {directory}: {e}")
        return []


def validate_script_structure(script_content: str, tool_name: str, tool_type: str) -> Dict[str, Any]:
    """
    Validates the script structure to ensure it contains the expected elements.
    """
    expected_elements = [
        f"tool_type_for_Tool_Manager = \"{tool_type}\"",
        f"{tool_name}_description_json = {{",
        f"{tool_name}_description_short_str = \"..."
    ]
    missing_elements = []
    for element in expected_elements:
        if element not in script_content:
            missing_elements.append(element)

    is_valid = len(missing_elements) == 0
    return {
        "is_valid": is_valid,
        "missing_elements": missing_elements
    }


def fix_script_structure(script_content: str, tool_name: str, tool_type: str) -> str:
    """
    Fixes the script structure by adding missing elements.
    """
    models = {
        "fix_structure": AIModel("You are an AI agent that fixes Python code structure.")
    }

    fix_structure_prompt = f"""
    The following script is missing some elements. Fix its structure:


    {script_content}


    Ensure the script includes:

    - `tool_type_for_Tool_Manager = "{tool_type}"`
    - `{tool_name}_description_json = {{ ... }}`
    - `{tool_name}_description_short_str = "..."`

    Provide the corrected script.
    """

    fixed_script = models["fix_structure"].send_message(fix_structure_prompt)
    print(f"🛠️  Script Structure Fix Stage: {fixed_script}")
    return fixed_script


def create_tool_external(tool_name: str, tool_type: str, tool_description: str,arguments: str,
                         loop: int = 0) -> \
        Dict[str, Any]:
    """
    External function for AI-driven tool creation.
    """
    models = {
        "design": AIModel(
            "You are an AI agent designing a new Python tool.  You must  consider  that  all  new  tools will be saved in tools/ai_gnerated_tools folder.  The tool  must   have  this structure: \n"
            "tool_type_for_Tool_Manager = \"{tool_type}\"\n"
            "\n"
            "# Your code here ...\n"
            "\n"
            "{tool_name}_description_json = {{\n"
            "    'function_declarations': [\n"
            "        {{\n"
            "            'name': '{tool_name}',\n"
            "            'description': '...',\n"
            "            'parameters': {{\n"
            "                'type_': 'OBJECT',\n"
            "                'properties': {{\n"
            "                    ...\n"
            "                }},\n"
            "                'required': [...]\n"
            "            }}\n"
            "        }}\n"
            "    ]\n"
            "}}\n"
            "\n"
            "{tool_name}_description_short_str = \"...\"\n"
            "\n"
            "#end"),
        "implementation": AIModel("You are an AI agent that writes clean and efficient Python code."),
        "review": AIModel("You are an AI code reviewer."),
        "description": AIModel("You are an AI agent creating JSON descriptions for tools."),
        "check": AIModel(
            "You are an AI agent that checks if the code has the correct structure and fixes it if it doesn't."),
        "final": AIModel(
            "You are an AI agent that generates the final code with all the necessary elements. remember  that  the saveing  folder  is tools/ai_generated_tools  remember  not to use  spaces in naming  use _ instead"),
        "sanity_check": AIModel(
            "You are an AI agent that checks Python code for basic errors and potential issues. If you find problems, provide a corrected version. If the code looks good, say 'No issues found'.")
    }

    # Design stage
    print(f"\033[92m Design Stage:\033[0m")
    design_prompt = f"Design a Python tool named '{tool_name}' of type '{tool_type}' that meat  that  description: {tool_description}. "
    design_prompt += f"It should take these parameters: {arguments}. "
    design_prompt += "**The tool should be implemented as a function.**  This function should encapsulate all the necessary functionality, including any class instantiation required. "
    design_prompt += "The function should be callable externally and return the desired results."
    design_prompt += "classes should  not  be  passed  as  parametrs  use  strings  instead"

    design = models["design"].send_message(design_prompt)
    print(f"\033[92m✨  Design Stage:  {design}\033[0m")

    # Implementation stage
    print(f"\033[92m💻  Implementation Stage:\033[0m")
    implementation_prompt = f"Implement the following tool design:\n\n{design}\n\nEnsure the code is clean, efficient, and well-documented. Include a tool_type_for_Tool_Manager variable."
    implementation = models["implementation"].send_message(implementation_prompt)
    print(f"\033[92m💻  Implementation Stage:  {implementation}\033[0m")

    # Review stage
    print(f"\033[92m🧐  Review Stage:\033[0m")
    review_prompt = f"Review the following code implementation:\n\n{implementation}\n\nProvide feedback and suggestions for improvement."
    review = models["review"].send_message(review_prompt)
    print(f"\033[92m🧐  Review Stage:  {review}\033[0m")

    # Final implementation
    print(f"\033[92m✅  Final Implementation Stage:\033[0m")
    final_implementation_prompt = f"""
    Update the code based on this review:\n\n{review}\n\nProvide the final implementation.
    Ensure the code follows this schema:
    remember  that  type is   always  type_
    remember that  varible  types are  always writen with Capital letters,Example string is STRING
    you will save  to file

    in 'description':  dont  use marks ( ) and  avoid  using '
    remember  that  type is always as  type_
    Schema:

    tool_type_for_Tool_Manager = "{tool_type}"

    # Your code here ...

    def {tool_name}({arguments}):
        # Your code here ...

    {tool_name}_description_json = {{
        'function_declarations': [
            {{
                'name': '{tool_name}',
                'description': '...',
                'parameters': {{
                    'type_': 'OBJECT',
                    'properties': {{
                        ...
                    }},
                    'required': [...]
                }}
            }}
        ]
    }}

    {tool_name}_description_short_str = "..."

    #end
    """
    final_implementation = models["implementation"].send_message(final_implementation_prompt)
    print(f"\033[92m✅  Final Implementation Stage:  {final_implementation}\033[0m")

    if loop == 1:
        # Loop for improvements
        print("\033[93m🚀  Entering improvement loop...\033[0m")
        while True:
            # Check Script Structure
            print(f"\033[92m✅  Check Stage:\033[0m")
            check_prompt = f"""
            Check if the following code has the correct structure. If it doesn't, fix it.


            {final_implementation}


            #The code should have schema
            #start
             tool_type_for_Tool_Manager = "{tool_type}"

             def {tool_name} implementation

             {tool_name}_description_json = {{ ... }}
             {tool_name}_description_short_str = "..."
            #end



             you  must   remember  that  the  name of  the  scipt should  be  the   name of  main fucction in the tool: {tool_name}!!!

            """
            checked_implementation = models["check"].send_message(check_prompt)
            print(f"\033[92m✅  Check Stage:  {checked_implementation}\033[0m")

            # Finalize the code
            print(f"\033[92m✅  Final Stage:\033[0m")
            final_prompt = f"""
            Generate the final code for the tool '{tool_name}' based on this implementation:

            ```python
            {checked_implementation}
            ```

            Make sure the code is well-formatted, documented, and includes all the necessary elements:

            #start
             tool_type_for_Tool_Manager = "{tool_type}"

             def {tool_name} implementation

             {tool_name}_description_json = {{ ... }}
             {tool_name}_description_short_str = "..."
            #end


            also  when comes    to json description
            any defoautls  should be written in descritpion not  as separated entry
            information about  returns should be in  desirption nos  as separated  entry


            """
            final_code = models["final"].send_message(final_prompt)
            print(f"\033[92m✅  Final Stage:  {final_code}\033[0m")

            # Improvement Loop Prompts (DIVERSE QUESTIONS)
            print(f"\033[92m🧐  Improvement Stage:\033[0m")
            improvement_prompt = f"""
            Review the following code:

            ```python
            {final_code}
            ```

            remember  that  final code  should  not   have  ```python      ```

            Answer these questions:

            1. Are there any errors or bugs in the code? If so, provide a corrected version.
            2. Can the code be made more efficient or readable? If so, provide a revised version.
            3. Are there any missing features or functionalities that should be added? If so, describe them.
            4. Is the code keeping  the correct  schema ? If not, suggest improvements.
            5. Is the tool fulfilling the original design requirements? If not, describe how to improve it.
            6. pay attention to varible names, function  name, name of the file,  n
            7. instead spaces in naming  use _  instead , use  only small letters for  naming

            If you are satisfied with the code, type "**DONE**" and save final code.
            """
            improvement_response = models["review"].send_message(improvement_prompt)
            print(f"\033[92m🧐  Improvement Stage:  {improvement_response}\033[0m")

            done_variations = ["DONE", "Done", "done", "dOne", "DoNe", " **DONE** ", " **Done** ",
                               " **done** "]  # Add variations with spaces

            if any(variation in improvement_response.upper() for variation in done_variations):
                break
            else:
                final_implementation = improvement_response

    # Create JSON description
    print(f"\033[92m📝  JSON Description Stage:\033[0m")
    json_description_prompt = f"""
    Create a JSON description for the tool '{tool_name}' based on this implementation:

    {final_implementation}

    The JSON should follow this structure: remember  that  type is  always  type_   and  that varible  types  are  always   written with capital letters, remember  that   new  python tools  must  be  saved in tools  folder
    {{
        "function_declarations": [
            {{
                "name": "{tool_name}",
                "description": "...",
                "parameters": {{
                    "type_": "OBJECT",
                    "properties": {{
                        ...
                    }},
                    "required": [...]
                }}
            }}
        ]
    }}
    """
    json_description = models["description"].send_message(json_description_prompt)
    print(f"\033[92m📝  JSON Description Stage:  {json_description}\033[0m")

    # Save the final implementation to a file
    filename = f"{tool_name}.py"
    save_success = save_to_file(final_implementation, filename)

    if save_success:
        print(f"\033[92m💾  Save Success:\033[0m")
        print(f"\033[92m💾  Save Success:  {save_success}\033[0m")

        # Sanity Check
        print(f"\033[92m🔎  Sanity Check Stage:\033[0m")
        with open(f"tools/ai_generated_tools/{filename}", 'r') as f:
            saved_code = f.read()
        sanity_check_prompt = f"Check the following code for basic errors or potential issues: ```python\n{saved_code}\n``` If you find problems, provide a corrected version. If the code looks good, say 'No issues found'."
        sanity_check_result = models["sanity_check"].send_message(sanity_check_prompt)
        print(f"\033[92m🔎  Sanity Check Result:  {sanity_check_result}\033[0m")

        # Validate and fix the saved script
        validation_result = validate_script_structure(saved_code, tool_name, tool_type)
        if not validation_result['is_valid']:
            print(f"\033[92m🛠️ Fixing script structure for {filename}:\033[0m")
            fixed_script = fix_script_structure(saved_code, tool_name, tool_type)
            save_to_file(fixed_script, filename)  # Save the fixed script
    else:
        print(f"\033[91m❌ Save Failed:\033[0m")

    # Check files in the current directory
    print(f"\033[92m📁  Files in Directory:\033[0m")
    files_in_directory = check_files()
    print(f"\033[92m📁  Files in Directory:  {files_in_directory}\033[0m")

    return {
        "tool_name": tool_name,
        "tool_type": tool_type,
        "design": design,
        "implementation": final_implementation,
        "review": review,
        "json_description": json_description,
        "save_success": save_success,
        "files_in_directory": files_in_directory
    }


# JSON description for create_tool_external
create_tool_external_description_json = {
    'function_declarations': [
        {
            'name': 'create_tool_external',
            'description': 'creates python tools  uinsg ai, and function calling, the funcion is good to create  scipts  that will be used by  the ai system, it is using a few steps of ai  models to create  given tool',
            'parameters': {
                'type_': 'OBJECT',
                'properties': {
                    'tool_name': {
                        'type_': 'STRING',
                        'description': 'Name of the tool to be created'
                    },

                    'tool_type': {
                        'type_': 'STRING',
                        'description': 'Type of the tool: os,focus,all,web'
                    },
                    'tool_description': {
                        'type_': 'STRING',
                        'description': 'Description  of  the  tool to create, this  should  be  ditailed'
                    },
                    'arguments': {
                        'type_': 'STRING',
                        'description': 'Parameters that the tool should accept'
                    },
                    'loop': {
                        'type_': 'INTEGER',
                        'description': 'Whether to enable an improvement loop 1 for yes, 0 for no, its better to use 1'
                    }
                },
                'required': ['tool_name', 'tool_type', 'tool_description', 'arguments']
            }
        }
    ]
}

create_tool_external_description_short_str = "Creates a new Python tool using AI-driven processes, including design, implementation, review, structure validation, and JSON description generation, with optional improvement loop."