import time
import datetime
import re
import os

import google.generativeai as genai
from termcolor import colored

genai.configure(api_key='YOUR_API_KEY_HERE')

# --- Memory Categories ---
categories = {
    "Actions and Results": {
        "past": ["Actions Taken", "Results Observed"],
        "present": ["Current Actions", "Ongoing Results"],
        "future": ["Planned Actions", "Anticipated Results"]
    },
    "Things": {
        "past": ["Objects Encountered", "Places Visited", "Concepts Learned"],
        "present": ["Current Objects", "Current Location", "Concepts Applied"],
        "future": ["Desired Objects", "Planned Locations", "Future Applications"]
    },
    "OwnState": {
        "past": ["Emotional State", "Physical State", "Mental State", "Spiritual State"],
        "present": ["Current Emotional State", "Current Physical State",
                    "Current Mental State", "Current Spiritual State"],
        "future": ["Anticipated Emotional State", "Desired Physical State",
                   "Expected Mental State", "Spiritual Goals"]
    },
    "Paradoxes and Contradictions": {
        "past": ["Past Paradoxes", "Past Internal Conflicts", "Past Cognitive Dissonance"],
        "present": ["Current Paradoxes", "Ongoing Internal Conflicts", "Current Cognitive Dissonance"],
        "future": ["Potential Paradoxes", "Expected Internal Conflicts",
                   "Strategies to Address Dissonance"]
    },
    "Living Things": {
        "past": ["Past Human Interactions", "Past Animal Encounters",
                 "Past Nature Experiences"],
        "present": ["Current Relationships", "Current Animal Interactions",
                    "Current Nature Experiences"],
        "future": ["Future Relationships", "Anticipated Animal Encounters",
                   "Planned Nature Experiences"]
    }
}
def create_file_structure():
    """Creates the file structure for storing memories."""
    for category in categories:
        for time_period in ["past", "present", "future"]:
            for subcategory in categories[category][time_period]:
                folder_path = os.path.join("memories", category, time_period, subcategory)
                os.makedirs(folder_path, exist_ok=True)
create_file_structure()

# --- MemoryLog Class ---
class MemoryLog:
    """
    A class to represent a single memory entry in a MemoryLog.
    """

    def __init__(self, memory_id, about, time, interaction_type, result, positive_impact, negative_impact, expectations,
                 object_states, short_description, details={}, category=None, subcategory=None, intensity=None,
                 duration=None, objects=[], people=[], conclusion=None, interactions=[], timestamp=None):
        self.memory_id = memory_id
        self.about = about
        self.time = time if isinstance(time, datetime.datetime) else datetime.datetime.strptime(time, "%Y-%m-%d")
        self.interaction_type = interaction_type
        self.result = result
        self.positive_impact = positive_impact
        self.negative_impact = negative_impact
        self.expectations = expectations
        self.object_states = object_states
        self.short_description = short_description
        self.details = details
        self.category = category
        self.subcategory = subcategory
        self.intensity = intensity
        self.duration = duration
        self.objects = objects
        self.people = people
        self.conclusion = conclusion
        self.interactions = interactions

    def __str__(self):
        """Returns a formatted string representation of the memory."""
        output = f"""
        Memory ID: {self.memory_id}
        About: {self.about}
        Time: {self.time.strftime("%Y-%m-%d")}
        Interaction Type: {self.interaction_type}
        Result: {self.result}
        Positive Impact: {self.positive_impact}
        Negative Impact: {self.negative_impact}
        Expectations: {self.expectations}
        Object States: {self.object_states}
        Short Description: {self.short_description}
        Category: {self.category}
        Subcategory: {self.subcategory}
        Intensity: {self.intensity}
        Duration: {self.duration}
        Objects: {self.objects}
        People: {self.people}
        Conclusion: {self.conclusion}
        Interactions: {self.interactions}
        Details: {self.details}
        """
        return output


# --- Function to Create File Structure ---
def create_file_structure():
    """Creates the file structure for storing memories."""
    for category in categories:
        for time_period in ["past", "present", "future"]:
            for subcategory in categories[category][time_period]:
                folder_path = os.path.join("memories", category, time_period, subcategory)
                os.makedirs(folder_path, exist_ok=True)


# --- Function to Generate Random Interaction Prompt ---
def generate_random_interaction_prompt():
    interaction_types = ["Social", "Learning", "Creative", "Physical", "Spiritual"]
    topics = ["Science", "History", "Art", "Nature", "Technology",
              "Philosophy", "Fiction"]

    interaction_type = interaction_types[int(time.time() % len(interaction_types))]
    topic = topics[int(time.time() % len(topics))]

    prompt = (f"You are a system interacting with a user. The user wants to "
              f"engage in a {interaction_type} interaction about {topic}. "
              f"What would you say?")
    return prompt


def store_memory(memory_log_details: dict, conversation_context: str = ""):
    """Stores a memory log entry in the appropriate file."""
    print(f"{colored('Storing Memory:', 'green')}")

    # Create MemoryLog object
    memory_log = MemoryLog(
        memory_id=memory_log_details.get("memory_id",
                                         f"Memory_{int(time.time())}"),
        about=memory_log_details.get("About", "Unknown"),
        time=memory_log_details.get("Time",
                                    datetime.datetime.now().strftime("%Y-%m-%d")),
        interaction_type=memory_log_details.get("Interaction Type", "Unknown"),
        result=memory_log_details.get("Result", "Unknown"),
        positive_impact=memory_log_details.get("Positive Impact", "Unknown"),
        negative_impact=memory_log_details.get("Negative Impact", "Unknown"),
        expectations=memory_log_details.get("Expectations", "Unknown"),
        object_states=memory_log_details.get("Object States", "Unknown"),
        short_description=memory_log_details.get("Short Description",
                                                 "Unknown"),
        details=memory_log_details.get("Details", {})
    )

    # --- Get category and subcategory from memory_log_details ---
    category = memory_log_details.get("Category", "Unknown").replace(" ", "_")
    subcategory = memory_log_details.get("Subcategory", "Unknown").replace(" ", "_")

    # --- Validate Category and Subcategory ---
    if category not in categories:
        print(f"{colored('Error:', 'red')} Invalid category: {category}")
        return  # Stop execution if category is invalid

    if subcategory not in categories[category]['past']:
        print(f"{colored('Error:', 'red')} Invalid subcategory: {subcategory} for category: {category}")
        return  # Stop execution if subcategory is invalid

    # Create Date-Based Filename and Save
    timestamp = datetime.datetime.now().strftime("%Y%m%d")
    memory_count = (len(os.listdir(os.path.join("memories", category,
                                                "past", subcategory))) + 1)
    filename = f"{timestamp}_{memory_count:03d}.txt"

    folder_path = os.path.join("memories", category, "past", subcategory)
    filepath = os.path.join(folder_path, filename)

    with open(filepath, 'w') as f:
        f.write(str(memory_log))

    print(f"Memory saved to: {filepath}")


def RESPONSE_INTERPRETER_FOR_FUNCION_CALLING(response):  # Pass tool_manager here
    """Interprets the model's response, extracts function details, and executes the appropriate function."""

    print(f"---------------RESPONSE_INTERPRETER_FOR_FUNCION_CALLING START----------------------")
    Multiple_ResultsOfFunctions_From_interpreter = []

    if response.candidates:
        for part in response.candidates[0].content.parts:
            if hasattr(part, 'function_call'):
                function_call = part.function_call
                function_name = function_call.name
                function_args = function_call.args

                # Get the function from the tool manager
                function_to_call = globals().get(function_name)

                if function_to_call:  # Check if the tool function is found
                    print(f"FUNCTION CALL: {function_name}({function_args}) ")

                    try:
                        results = function_to_call(**function_args)
                    except TypeError as e:
                        results = f"TypeError: {e}"
                    except Exception as e:
                        results = f"Exception: {e}"

                    function_name_arguments = f"{function_name}({function_args})"
                    modified_results = f"Result of Called function {function_name_arguments}: {results}"
                    Multiple_ResultsOfFunctions_From_interpreter.append(modified_results)
                else:
                    print(f"Warning: Tool function '{function_name}' not found.")

    return Multiple_ResultsOfFunctions_From_interpreter


# --- Main Function ---
def main():
    # Interaction History Generator Model
    interaction_model = genai.GenerativeModel(
        system_instruction=("You follow orders and generate creative text "
                            "interactions."),
        model_name='gemini-1.5-flash-latest',
        safety_settings={'HARASSMENT': 'block_none'}
    )

    chat1 = interaction_model.start_chat
    prompt = generate_random_interaction_prompt
    response1 = chat1.send_message(prompt)

    # --- Tool Description for AI Model ---
    store_memory_description = {
        'function_declarations': [
            {
                'name': 'store_memory',
                'description': ('Stores a memory log entry in the appropriate file '
                                'based on its category and time.'),
                'parameters': {
                    'type_': 'object',
                    'properties': {
                        'memory_log_details': {
                            'type': 'object',
                            'description': ('A dictionary containing the memory details. '
                                            'Required keys: category, subcategory, about, time, '
                                            'interaction_type, result, positive_impact, negative_impact, '
                                            'expectations, object_states, short_description. '
                                            'Optional keys: details, intensity, duration, objects, people, '
                                            'conclusion, interactions.'),
                            'required': ['category', 'subcategory', 'about', 'time', 'interaction_type',
                                         'result', 'positive_impact', 'negative_impact', 'expectations',
                                         'object_states', 'short_description']
                        },
                        'conversation_context': {
                            'type': 'string',
                            'description': 'The full conversation history up to this point.',
                        },
                    },
                    'required': ['memory_log_details', 'conversation_context']
                },
            }
        ]
    }
    # Memory Creation Model
    memory_model = genai.GenerativeModel(
        system_instruction=f"""You are a system that creates memory logs. 
                    You are provided with interaction history. 
                    Use the 'store_memory' tool to store memories.

                    Memory Log Format:
                    - Category: [category]
                    - Subcategory: [subcategory]
                    - About: [brief description]
                    - Time: [timestamp]
                    - Interaction Type: [interaction type]
                    - Result: [success/failure/ongoing]
                    - Positive Impact: [positive outcomes]
                    - Negative Impact: [negative outcomes]
                    - Expectations: [expectations prior to the interaction]
                    - Object States: [objects/locations involved]
                    - Short Description: [brief summary]
                    - Details: [optional additional information]

                    now  the possilbe  placess where  to  save  it
                    categories = {
        "Actions and Results": {
        "past": ["Actions Taken", "Results Observed"],
                "present": ["Current Actions", "Ongoing Results"],
                "future": ["Planned Actions", "Anticipated Results"]
            },
            "Things": {
        "past": ["Objects Encountered", "Places Visited", "Concepts Learned"],
                "present": ["Current Objects", "Current Location", "Concepts Applied"],
                "future": ["Desired Objects", "Planned Locations", "Future Applications"]
            },
            "OwnState": {
        "past": ["Emotional State", "Physical State", "Mental State", "Spiritual State"],
                "present": ["Current Emotional State", "Current Physical State",
                            "Current Mental State", "Current Spiritual State"],
                "future": ["Anticipated Emotional State", "Desired Physical State",
                           "Expected Mental State", "Spiritual Goals"]
            },
            "Paradoxes and Contradictions": {
        "past": ["Past Paradoxes", "Past Internal Conflicts", "Past Cognitive Dissonance"],
                "present": ["Current Paradoxes", "Ongoing Internal Conflicts", "Current Cognitive Dissonance"],
                "future": ["Potential Paradoxes", "Expected Internal Conflicts",
                           "Strategies to Address Dissonance"]
            },
            "Living Things": {
        "past": ["Past Human Interactions", "Past Animal Encounters",
                         "Past Nature Experiences"],
                "present": ["Current Relationships", "Current Animal Interactions",
                            "Current Nature Experiences"],
                "future": ["Future Relationships", "Anticipated Animal Encounters",
                           "Planned Nature Experiences"]
            }
        }

                    Use  Function call to  save  that  memmory in proper  folder, with proper  data!
                    """,
        model_name='gemini-1.5-flash-latest',
        safety_settings={'HARASSMENT': 'block_none'},
        tools=[store_memory_description]
    )

    chat2 = interaction_model.start_chat
    response2 = chat2.send_message(prompt)

    intrpreterResult = RESPONSE_INTERPRETER_FOR_FUNCION_CALLING(response2)

    # Create Memory File Structure
    create_file_structure()

    # --- Memory Creation Loop ---
    iteration_count = 0

    print(f"{colored('Iteration:', 'yellow')} {iteration_count}")
    iteration_count += 1

    # Generate Creative Writing Prompt
    chat_creative_writing = interaction_model.start_chat(history=[])
    creative_prompt = "Create a random story, experience, or action - anything you like."
    print(f"{colored('Creative Writing Prompt:', 'cyan')} {creative_prompt}")
    creative_response = chat_creative_writing.send_message(creative_prompt)
    print(f"Creative Output: {colored(creative_response.text, 'green')}")

    # Create Memory from Creative Output
    memory_chat = memory_model.start_chat(history=[])
    memory_prompt = (f"Create a memory log entry and save it in the "
                     f"proper folder using the 'store_memory' function. "
                     f"Base the memory on this: \n{creative_response.text}")
    print(f"{colored('Memory Creation Prompt:', 'blue')} {memory_prompt}")
    memory_response = memory_chat.send_message(memory_prompt)

    # Interpret and execute function call
    RESPONSE_INTERPRETER_FOR_FUNCION_CALLING(memory_response)