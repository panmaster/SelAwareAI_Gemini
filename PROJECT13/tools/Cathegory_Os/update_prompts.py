# UpdatePrompts.py
import os
tool_type_for_Tool_Manager="reflection"
import json

# ANSI escape codes for colors
RESET = "\033[0m"
BLUE = "\033[34m"
GREEN = "\033[32m"
RED = "\033[31m"

def update_prompts(prompt_key: str, new_prompt: str) -> dict:
    """Updates a prompt in the prompts.json file."""

    print(f"{BLUE}Entering: UpdatePrompts(...) {RESET}")
    try:
        # Load existing prompts
        with open("Brain_settings/prompts.json", 'r') as file:
            prompts = json.load(file)

        # Update the specified prompt
        prompts[prompt_key] = new_prompt

        # Save updated prompts
        with open("Brain_settings/prompts.json", 'w') as file:
            json.dump(prompts, file, indent=4)

        success_message = f"Prompt '{prompt_key}' updated successfully."
        print(f"{GREEN}{success_message} {RESET}")
        print(f"{BLUE}Exiting: UpdatePrompts(...) {RESET}")
        return {"status": "success", "message": success_message}

    except FileNotFoundError:
        error_message = f"File 'prompts.json' not found."
        print(f"{RED}{error_message} {RESET}")
        print(f"{BLUE}Exiting: UpdatePrompts(...) {RESET}")
        return {"status": "failure", "message": error_message}

    except KeyError:
        error_message = f"Prompt '{prompt_key}' not found in 'prompts.json'."
        print(f"{RED}{error_message} {RESET}")
        print(f"{BLUE}Exiting: UpdatePrompts(...) {RESET}")
        return {"status": "failure", "message": error_message}

    except Exception as e:
        error_message = f"Failed to update prompt: {str(e)}"
        print(f"{RED}{error_message} {RESET}")
        print(f"{BLUE}Exiting: UpdatePrompts(...) {RESET}")
        return {"status": "failure", "message": error_message}


# Description for the Tool Manager
update_prompts_description_json = {
  "function_declarations": [
    {
      "name": "update_prompts",
      "description": "Updates a prompt in the 'prompts.json' file.",
      "parameters": {
        "type_": "OBJECT",
        "properties": {
          "prompt_key": {
            "type_": "STRING",
            "description": "The key of the prompt to update."
          },
          "new_prompt": {
            "type_": "STRING",
            "description": "The new value for the prompt."
          }
        },
        "required": ["prompt_key", "new_prompt"]
      }
    }
  ]
}
update_prompts_description_short_str = "Updates a prompt in the 'prompts.json' fil"