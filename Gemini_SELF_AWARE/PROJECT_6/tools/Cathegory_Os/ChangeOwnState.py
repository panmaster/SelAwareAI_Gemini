tool_type_for_Tool_Manager="reflection"

import os
import json
from typing import Any, Dict, List, Union

# Define ANSI escape codes for colored output (optional but enhances readability)
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

# --- Constants ---
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
STATE_FILE_PATH = os.path.abspath(os.path.join(SCRIPT_DIR, '../../Brain_settings/State_of_mind.json'))


# --- State Management Functions ---
def _load_state() -> Dict[str, Any]:
    """Loads the current state from the JSON file.
    Handles potential errors gracefully.
    """
    try:
        with open(STATE_FILE_PATH, "r") as file:
            return json.load(file)
    except FileNotFoundError:
        print(f"{YELLOW}Warning: State file not found at '{STATE_FILE_PATH}'. Returning an empty state.{RESET}")
        return {}  # Return an empty dictionary if the file is not found
    except json.JSONDecodeError:
        print(f"{RED}Error: State file is corrupted. Returning an empty state.{RESET}")
        return {}  # Return an empty dictionary if the JSON is invalid


def _save_state(state: Dict[str, Any]) -> None:
    """Saves the given state to the JSON file."""
    try:
        with open(STATE_FILE_PATH, "w") as file:
            json.dump(state, file, indent=4)
    except PermissionError:
        print(f"{RED}Error: Permission denied when saving the state file. Check file permissions.{RESET}")
    except Exception as e:
        print(f"{RED}Error: An unexpected error occurred while saving the state: {e}{RESET}")


def _initialize_state() -> None:
    """Initializes the state file with default values
    if it doesn't exist.
    """
    if not os.path.exists(STATE_FILE_PATH):
        initial_state = {
            "FocusOn": "",
            "FocusLevel": 0,
            "Defocus": "",
            "FrustrationLevel": 0,
            "CurrentCostOfProgress": 0,
            "Short_term_goals": [],
            "Long_term_goals": [],
            "Accomplished": []
        }
        _save_state(initial_state)
        print(f"{GREEN}State file initialized successfully at '{STATE_FILE_PATH}'.{RESET}")


# --- Main State Change Function ---
def ChangeOwnState(
        FocusOn: str = None,
        FocusLevel: float = None,
        Defocus: str = None,
        FrustrationLevel: float = None,
        CurrentCostOfProgress: float = None,
        Short_term_goals: Union[str, List[str]] = None,
        Long_term_goals: Union[str, List[str]] = None,
        Accomplished: Union[str, List[str]] = None,
) -> str:
    """
    Updates the state of the model stored in 'State_of_mind.json'.
    Provides detailed error messages and handles different input types.

    Args:
        FocusOn (str, optional): The current area or topic of focus.
        FocusLevel (float, optional): The intensity of focus (0 to 100).
        Defocus (str, optional): Areas or topics to shift focus away from.
        FrustrationLevel (float, optional): Level of frustration (0 to 100).
        CurrentCostOfProgress (float, optional): Perceived cost of progress (0 to 100).
        Short_term_goals (str or list, optional): A goal or list of goals to add.
        Long_term_goals (str or list, optional): A goal or list of goals to add.
        Accomplished (str or list, optional): A task or list of tasks to add.

    Returns:
        str: A message indicating success or the specific error encountered.
    """

    print(f"{CYAN}Entering ChangeOwnState function{RESET}")
    print(f"{CYAN}Parameters: FocusOn={FocusOn}, FocusLevel={FocusLevel}, Defocus={Defocus}, "
          f"FrustrationLevel={FrustrationLevel}, CurrentCostOfProgress={CurrentCostOfProgress}, "
          f"Short_term_goals={Short_term_goals}, Long_term_goals={Long_term_goals}, "
          f"Accomplished={Accomplished}{RESET}")

    # --- Input Validation ---
    def _validate_input(FocusLevel: float = None,
                        FrustrationLevel: float = None,
                        CurrentCostOfProgress: float = None) -> None:
        """Validates numeric input parameters to be between 0 and 100."""
        for param_name, param_value in [("FocusLevel", FocusLevel),
                                        ("FrustrationLevel", FrustrationLevel),
                                        ("CurrentCostOfProgress", CurrentCostOfProgress)]:
            if param_value is not None and (not isinstance(param_value, (int, float)) or not 0 <= param_value <= 100):
                raise ValueError(f"{param_name} must be a number between 0 and 100")

    try:
        # Validate numeric inputs
        _validate_input(FocusLevel, FrustrationLevel, CurrentCostOfProgress)

        # --- Load State ---
        state = _load_state()
        print(f"Current state: {json.dumps(state, indent=4)}")

        # --- Update State ---
        def _update_list_parameter(state: Dict, key: str, value: Union[str, List[str]]):
            """Helper function to update list parameters in the state."""
            if isinstance(value, str):
                state[key].append(value)
            elif isinstance(value, list) and all(isinstance(item, str) for item in value):
                state[key].extend(value)

        for key, value in {
            'FocusOn': FocusOn,
            'FocusLevel': FocusLevel,
            'Defocus': Defocus,
            'FrustrationLevel': FrustrationLevel,
            'CurrentCostOfProgress': CurrentCostOfProgress,
            'Short_term_goals': Short_term_goals,
            'Long_term_goals': Long_term_goals,
            'Accomplished': Accomplished
        }.items():
            if value is not None:
                if key in ['Short_term_goals', 'Long_term_goals', 'Accomplished']:
                    _update_list_parameter(state, key, value)
                else:
                    state[key] = value

        # --- Save Updated State ---
        _save_state(state)

        print(f"Updated state: {json.dumps(state, indent=4)}")
        return f"{BRIGHT_BLUE}State_of_mind.json updated successfully!{RESET}"

    except ValueError as e:
        print(f"{RED}Input Error: {e}{RESET}")
        return f"Input error: {str(e)}"  # Return a more specific error message
    except Exception as e:
        print(f"{RED}Unexpected Error: {e}{RESET}")
        return f"Unexpected error: {str(e)}"

    # --- Initialize on Startup ---


ChangeOwnState_description_json = {
    "function_declarations": [
        {
            "name": "ChangeOwnState",
            "description": "Updates the state of the model stored in 'State_of_mind.json'. "
                           "Provide values for parameters you want to update. "
                           "For list parameters, provide a string to add a single item or a list of strings to add multiple items.",
            "parameters": {
                "type_": "OBJECT",
                "properties": {
                    "FocusOn": {
                        "type_": "STRING",
                        "description": "Specifies the current area or topic of focus.",
                    },
                    "FocusLevel": {
                        "type_": "INTEGER", # You can use "NUMBER" for both int and float
                        "description": "Defines the intensity of focus on a scale of 0 to 100.",
                    },
                    "Defocus": {
                        "type_": "STRING",
                        "description": "Specifies areas or topics to shift focus away from.",
                    },
                    "FrustrationLevel": {
                        "type_": "INTEGER", # You can use "NUMBER" for both int and float
                        "description": "Represents the current level of frustration on a scale of 0 to 100.",
                    },
                    "CurrentCostOfProgress": {
                        "type_": "INTEGER", # You can use "NUMBER" for both int and float
                        "description": "Indicates the perceived cost of making progress on a scale of 0 to 100.",
                    },
                    "Short_term_goals": {
                        "type_": "ARRAY",
                        "items": {"type_": "STRING"},
                        "description": "A string or list of short-term goals to append to the existing list.",
                    },
                    "Long_term_goals": {
                        "type_": "ARRAY",
                        "items": {"type_": "STRING"},
                        "description": "A string or list of long-term goals to append to the existing list.",
                    },
                    "Accomplished": {
                        "type_": "ARRAY",
                        "items": {"type_": "STRING"},
                        "description": "A string or list of accomplished tasks to append to the existing list.",
                    }
                },
            }
        }
    ]
}

ChangeOwnState_description_short_str = "Updates the state in 'State_of_mind.json'. For list parameters, you can provide a single string or a list of strings to be appended."














#_initialize_state()

# Example usage:
# ChangeOwnState(FocusOn="Coding", FocusLevel=80, Short_term_goals=["Finish function", "Write tests"])