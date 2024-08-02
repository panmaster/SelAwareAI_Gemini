# tools/os/update_own_config.py
tool_type_for_TOOL_MANAGER = "os"
update_own_config_short_description = """Updates the AI's own configuration file (config.json)."""

import json
import os

def update_own_config(config_path: str = "CONFIG/config.json", **kwargs) -> dict:
    """
    Updates the AI's own configuration file (config.json).

    Available Parameters:

    General Parameters:
        - loop_type (str): Type of loop ('fixed' or 'infinite').
        - num_loops (int): Number of loops to execute in a 'fixed' loop.
        - max_loops (int): Maximum number of loops allowed, even in an 'infinite' loop.

    Model-Specific Parameters (for each model in the `models` list):
        - model_ID (str): Unique identifier for the model.
        - model_name (str): Name of the Gemini Pro model to use (e.g., "gemini-1.5-pro-exp-0801").
        - system_instruction (str): System instructions for the model, guiding its behavior.
        - allowed_tools (list): List of allowed tool names for the model (e.g., ["all", "web", "os"]).
        - prompt_injector (str): Text to be injected into the prompt before sending it to the model.
        - loadFocus (bool): Whether to load the focus data for the model.
        - generateAudio (bool): Whether to generate audio output for the model's responses.
        - useFlags (bool): Whether to use flags for controlling loop termination (e.g., STOP flags).
        - flagTypes (list): List of flag types to use (e.g., ["STOP_FLAGS"]).
        - STOP_FLAGS_instruction (str): Instructions for how to use STOP flags.
        - STOP_FLAGS_pattern (str): Regular expression pattern for detecting STOP flags.

    Args:
        config_path (str, optional): Path to the config.json file. Defaults to "CONFIG/config.json".
        **kwargs: Key-value pairs representing the configuration parameters to be updated.

    Returns:
        dict: A dictionary containing the status of the operation and a message.
    """
    try:
        with open(config_path, "r") as f:
            config = json.load(f)

        for key, value in kwargs.items():
            # Basic validation (you might want to add more robust validation)
            if key == "loop_type" and value not in ["fixed", "infinite"]:
                return {"status": "failure", "message": "Invalid loop_type. Must be 'fixed' or 'infinite'."}

            # For model-specific parameters, you'll need to iterate through the `models` list
            # and find the model with the matching `model_ID` to update its parameters.

            config[key] = value

        with open(config_path, "w") as f:
            json.dump(config, f, indent=4)

        return {"status": "success", "message": f"Configuration updated successfully."}
    except Exception as e:
        return {"status": "failure", "message": f"Error updating configuration: {str(e)}"}