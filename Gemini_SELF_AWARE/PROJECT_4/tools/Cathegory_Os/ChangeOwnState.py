import os
import json
class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

MAGENTA = bcolors.OKCYAN
YELLOW = bcolors.OKGREEN
BRIGHT_YELLOW = bcolors.WARNING
PURPLE = bcolors.OKBLUE
BLUE = bcolors.BOLD
def initializeState():
    """
    Initializes the state file 'State_of_mind.json' with default values.

    Creates the 'Brain_settings' directory if it doesn't exist.
    """
    script_dir = os.path.dirname(os.path.abspath(__file__))
    state_file_path = os.path.abspath(os.path.join(script_dir, '../../Brain_settings/State_of_mind.json'))
    print(f" Initializing state at: {state_file_path}")

    state_dir = os.path.dirname(state_file_path)
    if not os.path.exists(state_dir):
        os.makedirs(state_dir)
        print(" Created directory for state file.")

    state = {
        "FocusOn": "",
        "FocusLevel": 0,
        "Defocus": "",
        "FrustrationLevel": 0,
        "CurrentCostOfProgress": 0,
        "Short_term_goals": [],
        "Long_term_goals": [],
        "Accomplished": []
    }

    with open(state_file_path, "w") as file:
        json.dump(state, file, indent=4)

    print(" State initialized.")

def ChangeOwnState(FocusOn=None, FocusLevel=None, Defocus=None, FrustrationLevel=None, CurrentCostOfProgress=None,
                   Short_term_goals=None, Long_term_goals=None, Accomplished=None):

    print(f"\n{MAGENTA}****************  ENTERED ChangeOwnState *******************\n")
    print(
        f"{YELLOW} Parameters: FocusOn: {FocusOn}, FocusLevel: {FocusLevel}, Defocus: {Defocus}, FrustrationLevel: {FrustrationLevel}, CurrentCostOfProgress: {CurrentCostOfProgress}, Short_term_goals: {Short_term_goals}, Long_term_goals: {Long_term_goals}, Accomplished: {Accomplished}")

    script_dir = os.path.dirname(os.path.abspath(__file__))
    state_file_path = os.path.abspath(os.path.join(script_dir, '../../Brain_settings/State_of_mind.json'))
    print(f"{BRIGHT_YELLOW} State file path: {state_file_path}")

    if not os.path.exists(state_file_path):
        print(f"{PURPLE} State file does not exist. Initializing state.")
        initializeState(state_file_path)

    try:
        with open(state_file_path, "r") as file:
            state = json.load(file)
        print(f"{BLUE} Current state: {json.dumps(state, indent=4)}")

        # Update the state based on provided parameters
        if FocusOn is not None:
            state["FocusOn"] = FocusOn
        if FocusLevel is not None:
            state["FocusLevel"] = FocusLevel
        if Defocus is not None:
            state["Defocus"] = Defocus
        if FrustrationLevel is not None:
            state["FrustrationLevel"] = FrustrationLevel
        if CurrentCostOfProgress is not None:
            state["CurrentCostOfProgress"] = CurrentCostOfProgress

        # Handle lists: Append or replace if provided
        if Short_term_goals is not None:
            state["Short_term_goals"] = Short_term_goals
        if Long_term_goals is not None:
            state["Long_term_goals"] = Long_term_goals
        if Accomplished is not None:
            state["Accomplished"] = Accomplished

        with open(state_file_path, "w") as file:
            json.dump(state, file, indent=4)

        print(f" Updated state: {json.dumps(state, indent=4)}")
        print("\n****************   FINISHED ChangeOwnState  *******************")
        return "State_of_mind.json updated"

    except Exception as e:
        print(f"{bcolors.FAIL}Error updating state: {e}{bcolors.ENDC}")
        return "Error updating state"

ChangeOwnState_description_json = {
    "function_declarations": [
        {
            "name": "ChangeOwnState",
            "description": "Updates the state of the model based on the provided parameters, which are used to adjust various aspects of its behavior: FocusOn, FocusLevel, Defocus, FrustrationLevel, CurrentCostOfProgress, Short_term_goals, Long_term_goals, Accomplished.",
            "parameters": {
                "type_": "OBJECT",
                "properties": {
                    "FocusOn": {
                        "type_": "STRING",
                        "description": "Specifies the area or topic to focus on."
                    },
                    "FocusLevel": {
                        "type_": "INTEGER",
                        "description": "Defines the intensity or level of focus."
                    },
                    "Defocus": {
                        "type_": "STRING",
                        "description": "Specifies the area or topic to defocus from."
                    },
                    "FrustrationLevel": {
                        "type_": "INTEGER",
                        "description": "Represents the current level of frustration."
                    },
                    "CurrentCostOfProgress": {
                        "type_": "INTEGER",
                        "description": "Indicates the current cost of progress in the task or activity."
                    },
                    "Short_term_goals": {
                        "type_": "ARRAY",
                        "description": "List of short-term goals."
                    },
                    "Long_term_goals": {
                        "type_": "ARRAY",
                        "description": "List of long-term goals."
                    },
                    "Accomplished": {
                        "type_": "ARRAY",
                        "description": "List of accomplished tasks."
                    }
                },
                "required": []
            }
        }
    ]
}

ChangeOwnState_description_short_str = "Updates the state in State_of_mind.json"

# Example usage:
initializeState()
ChangeOwnState(FocusOn="0",
               FocusLevel=0,
               Short_term_goals=[" "],
               Long_term_goals=[""])