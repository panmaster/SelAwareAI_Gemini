import os
import json

# Constants for file paths (adjust as needed)
PROMPTS_FILE = "Brain_settings/prompts.json"
EMOTIONS_FILE = "Brain_settings/emotions.json"
FOCUS_FILE = "Brain_settings/Focus.json"


def load_json(file_path):
    """Loads a JSON file and returns the data as a dictionary."""
    try:
        with open(file_path, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"Warning: File not found: {file_path}")
        return {}


def save_json(file_path, data):
    """Saves data to a JSON file."""
    with open(file_path, 'w') as f:
        json.dump(data, f, indent=2)


def load_prompts():
    """Loads prompts from the prompts.json file."""
    return load_json(PROMPTS_FILE)


def save_prompts(prompts):
    """Saves prompts to the prompts.json file."""
    save_json(PROMPTS_FILE, prompts)


def load_emotions():
    """Loads emotions from the emotions.json file."""
    return load_json(EMOTIONS_FILE)


def save_emotions(emotions):
    """Saves emotions to the emotions.json file."""
    save_json(EMOTIONS_FILE, emotions)


def load_state_of_mind():
    """Loads the state of mind from the Focus.json file."""
    return load_json(FOCUS_FILE)


def save_state_of_mind(state_of_mind):
    """Saves the state of mind to the Focus.json file."""
    save_json(FOCUS_FILE, state_of_mind)


def update_attachment(emotions, entity, value):
    """Updates the attachment value for a given entity."""
    if entity not in emotions["attachment"]:
        emotions["attachment"][entity] = 0
    emotions["attachment"][entity] += value
    emotions["attachment"][entity] = max(0, min(100, emotions["attachment"][entity]))
    return emotions


def get_focus_data():
    """Loads and returns focus data from the Focus.json file."""
    return load_state_of_mind()


def set_focus(focus_on):
    """Sets the focus in the Focus.json file."""
    state_of_mind = load_state_of_mind()
    state_of_mind["FocusOn"] = focus_on
    save_state_of_mind(state_of_mind)
    return f"Focus set to: {focus_on}"