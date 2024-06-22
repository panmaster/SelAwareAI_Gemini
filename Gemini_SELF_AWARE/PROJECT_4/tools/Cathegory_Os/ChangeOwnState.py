import os
import json


def initializeState():
    # Get the directory where this script is located
    script_dir = os.path.dirname(os.path.abspath(__file__))
    # Construct the full path to the JSON file (traversing 2 layers up)
    state_file_path = os.path.abspath(os.path.join(script_dir, '../../Brain_settings/State_of_mind.json'))

    # Ensure the Brain_settings directory exists
    state_dir = os.path.dirname(state_file_path)
    if not os.path.exists(state_dir):
        os.makedirs(state_dir)

    # Initialize state with default values
    state = {

        "FocusOn": "",
        "FocusLevel": "",
        "Defocus": "",
        "FrustrationLevel": "",
        "CurrentCostOfProgress": "0"
    }

    # Write initial state to file
    with open(state_file_path, "w") as file:
        json.dump(state, file, indent=4)


def ChangeOwnState( FocusOn=None, FocusLevel=None, Defocus=None,
                  FrustrationLevel=None, CurrentCostOfProgress=None):
    # Get the directory where this script is located
    script_dir = os.path.dirname(os.path.abspath(__file__))
    # Construct the full path to the JSON file (traversing 3 layers up)
    state_file_path = os.path.abspath(os.path.join(script_dir, '../../../Brain_settings/State_of_mind.json'))

     # Initialize state file if it doesn't exist
    if not os.path.exists(state_file_path):
        initializeState()

    # Load existing state
    with open(state_file_path, "r") as file:
        state = json.load(file)


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

    # Save the updated state
    with open(state_file_path, "w") as file:

        json.dump(state, file, indent=4)



ChangeOwnState_description_json =  {
    "function_declarations": [
        {
            "name": "ChangeOwnState",
            "description": "Updates the state of the model based on the provided parameters, which are used to adjust various aspects of its behavior.   FocusOn,FocusLevel, Defocus, FrustrationLevel, CurrentCostOfProgress, ",
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
                    }
                },
                "required": []
            }
        }
    ]
}
ChangeOwnState_description_short_str = "Updates the state in State_of_Mind"
