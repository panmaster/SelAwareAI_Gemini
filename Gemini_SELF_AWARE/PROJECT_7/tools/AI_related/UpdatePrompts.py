tool_type_for_Tool_Manager = "action"

import json
import os

PROMPTS_FILE = "stage_prompts.json"


def UpdatePrompts(stage: str, new_prompt: str) -> dict:
    """
    Updates the prompt for a specific stage in the AI's workflow.

    Args:
    stage (str): The stage to update ('input', 'reflection', or 'action')
    new_prompt (str): The new prompt text

    Returns:
    dict: A status message indicating success or failure
    """
    try:
        with open(PROMPTS_FILE, 'r') as f:
            prompts = json.load(f)

        if stage not in ['input', 'reflection', 'action']:
            return {"status": "error", "message": "Invalid stage. Use 'input', 'reflection', or 'action'."}

        prompts[stage] = new_prompt

        with open(PROMPTS_FILE, 'w') as f:
            json.dump(prompts, f, indent=2)

        return {"status": "success", "message": f"Updated {stage} prompt successfully."}
    except Exception as e:
        return {"status": "error", "message": str(e)}


UpdatePrompts_description_json = {
    'function_declarations': [
        {
            'name': 'UpdatePrompts',
            'description': 'Updates the prompt for a specific stage in the AI\'s workflow.',
            'parameters': {
                'type_': 'OBJECT',
                'properties': {
                    'stage': {'type_': 'STRING',
                              'description': "The stage to update ('input', 'reflection', or 'action')"},
                    'new_prompt': {'type_': 'STRING', 'description': 'The new prompt text'}
                },

            }
        }
    ]
}

UpdatePrompts_description_short_str = "Updates stage_prompts for different stages of the AI's workflow"