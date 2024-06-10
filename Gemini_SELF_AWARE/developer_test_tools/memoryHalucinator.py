import time
import datetime
import re
import os
import  google.generativeai as  genai
genai.configure(api_key='AIzaSyDEa1BAKI4ybj4N8Xloo4XY5uW5X62e-lw')
import google.generativeai as genai
from termcolor import colored, cprint

# ANSI escape codes for text colors
COLOR_CODES = {
    "red": "\033[91m",
    "green": "\033[92m",
    "yellow": "\033[93m",
    "blue": "\033[94m",
    "magenta": "\033[95m",
    "cyan": "\033[96m",
    "white": "\033[97m",
    "reset": "\033[0m",
}


def print_colored(text, color="white"):
    """Prints text with the specified color."""
    print(f"{COLOR_CODES.get(color, '')}{text}{COLOR_CODES['reset']}")


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
print_colored("Generated Memory Folders", "green")


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





def RESPONSE_INTERPRETER_FOR_FUNCION_CALLING(response):  # Pass tool_manager here
    """Interprets the model's response, extracts function details, and executes the appropriate function."""

    print_colored(f"---------------RESPONSE_INTERPRETER_FOR_FUNCION_CALLING START----------------------", "yellow")
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
                    print_colored(f"FUNCTION CALL: {function_name}({function_args}) ", "cyan")

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
                    print_colored(f"Warning: Tool function '{function_name}' not found.", "red")

    return Multiple_ResultsOfFunctions_From_interpreter


def store_memory(memory_log_details: dict, conversation_context: str = ""):
    """
    Stores a memory log entry in the appropriate file based on its category and time.
    The memory is saved within a hierarchical folder structure:

    - `memories` (root folder)
        - `category` (folder named after the "CATEGORY" parameter)
            - `past` (subfolder within the category folder)
                - `subcategory` (subfolder within the "past" folder named after the "SUBCATEGORY" parameter)

    The filename for the memory log entry is generated using the current date and a sequential counter.

    Args:
        memory_log_details (dict): A dictionary containing the memory details.
            Required keys:
                - CATEGORY (str): The category of the memory (e.g., "Personal", "Work"). The memory will be saved in a subfolder named after this category within the "memories/past" folder.
                - SUBCATEGORY (str): The subcategory of the memory (e.g., "Family", "Project"). The memory will be saved in a subfolder named after this subcategory within the "memories/past/category" folder.
                - ABOUT (str): A brief description of what the memory is about.
                - TIME (str): The timestamp of the memory.
                - INTERACTION_TYPE (str): The type of interaction associated with the memory.
                - RESULT (str): The outcome of the interaction.
                - POSITIVE_IMPACT (str): The positive impact of the memory.
                - NEGATIVE_IMPACT (str): The negative impact of the memory.
                - EXPECTATIONS (str): Expectations associated with the memory.
                - OBJECT_STATES (str): The state of objects involved in the memory.
                - SHORT_DESCRIPTION (str): A concise summary of the memory.
            Optional keys:
                - DETAILS (dict): A dictionary containing additional details about the memory.
                - INTENSITY (str): The intensity of the memory.
                - DURATION (str): The duration of the memory.
                - OBJECTS (list): A list of objects involved in the memory.
                - PEOPLE (list): A list of people involved in the memory.
                - CONCLUSION (str): A conclusion drawn from the memory.
                - INTERACTIONS (list): A list of interactions within the memory.
        conversation_context (str, optional): The full conversation history up to this point. Defaults to "".

    Returns:
        None
    """
    print_colored(f"Storing Memory:", "green")

    # Create MemoryLog object
    memory_log = MemoryLog(
        memory_id=memory_log_details.get("memory_id", f"Memory_{int(time.time())}"),
        about=memory_log_details.get("About", "Unknown"),
        time=memory_log_details.get("Time", datetime.datetime.now().strftime("%Y-%m-%d")),
        interaction_type=memory_log_details.get("Interaction Type", "Unknown"),
        result=memory_log_details.get("Result", "Unknown"),
        positive_impact=memory_log_details.get("Positive Impact", "Unknown"),
        negative_impact=memory_log_details.get("Negative Impact", "Unknown"),
        expectations=memory_log_details.get("Expectations", "Unknown"),
        object_states=memory_log_details.get("Object States", "Unknown"),
        short_description=memory_log_details.get("Short Description", "Unknown"),
        details=memory_log_details.get("Details", {})
    )

    # --- Get category and subcategory from memory_log_details ---
    category = memory_log_details.get("Category", "Unknown").replace(" ", "_")
    subcategory = memory_log_details.get("Subcategory", "Unknown").replace(" ", "_")

    # --- Validate Category and Subcategory ---
    if category not in categories:
        print_colored(f"Error: Invalid category: {category}", "red")
        return  # Stop execution if category is invalid

    if subcategory not in categories[category]['past']:
        print_colored(f"Error: Invalid subcategory: {subcategory} for category: {category}", "red")
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

    print_colored(f"Memory saved to: {filepath}", "blue")

    # Pretty Print Information about Memory Storage
    print_colored(f"Memory Details:", "cyan")
    print_colored(f"Category: {category}", "cyan")
    print_colored(f"Subcategory: {subcategory}", "cyan")
    print_colored(f"Filename: {filename}", "cyan")
    print_colored(f"Filepath: {filepath}", "cyan")

    # This section demonstrates how to access and print the memory details
    print_colored(f"Memory Content:", "cyan")
    print_colored(f"About: {memory_log.about}", "cyan")
    print_colored(f"Time: {memory_log.time}", "cyan")
    # ... print other details from memory_log as needed

    # Trigger the action based on the 'Trigger' parameter (assuming it exists)
    if 'Trigger' in memory_log_details:
        trigger = memory_log_details['Trigger']
        print_colored(f"Trigger: {trigger}", "magenta")
        # ... implement the trigger logic here ...


# Example usage (Replace with your actual memory data)
memory_details = {
    'Category': 'Personal',
    'Subcategory': 'Family',
    'About': 'Dinner with family',
    'Time': '2023-10-26',
    'Interaction_Type': 'Conversation',
    'Result': 'Pleasant',
    'Positive_Impact': 'Feeling connected',
    'Negative_Impact': 'None',
    'Expectations': 'Good time',
    'Object_States': 'Dinner table set',
    'Short_Description': 'Enjoyed dinner with family',
    # ... other optional keys ...
}

store_memory(memory_details)

STORE_MEMORY_DESCRIPTION = {
    'function_declarations': [
        {
            'name': 'store_memory',
            'description': 'Stores a memory log entry in a file within a hierarchical folder structure. '
                           'The structure is: `memories/category/past/subcategory`. The filename is '
                           'generated using the current date and a sequential counter.',
            'parameters': {
                'type_': 'OBJECT',
                'properties': {
                    'MEMORY_LOG_DETAILS': {
                        'type_': 'OBJECT',
                        'description': 'A dictionary containing the memory details.',
                        'required': [
                            'CATEGORY', 'SUBCATEGORY', 'ABOUT', 'TIME', 'INTERACTION_TYPE',
                            'RESULT', 'POSITIVE_IMPACT', 'NEGATIVE_IMPACT', 'EXPECTATIONS',
                            'OBJECT_STATES', 'SHORT_DESCRIPTION'
                        ],
                        'properties': {
                            'CATEGORY': {
                                'type_': 'STRING',
                                'description': 'The category of the memory (e.g., "Personal", "Work"). '
                                             'Determines the subfolder within `memories/past` where the memory is stored.'
                            },
                            'SUBCATEGORY': {
                                'type_': 'STRING',
                                'description': 'The subcategory of the memory (e.g., "Family", "Project"). '
                                             'Determines the subfolder within `memories/past/category` where the memory is stored.'
                            },
                            'ABOUT': {
                                'type_': 'STRING',
                                'description': 'A brief description of what the memory is about.'
                            },
                            'TIME': {
                                'type_': 'STRING',
                                'description': 'The timestamp of the memory.'
                            },
                            'INTERACTION_TYPE': {
                                'type_': 'STRING',
                                'description': 'The type of interaction associated with the memory.'
                            },
                            'RESULT': {
                                'type_': 'STRING',
                                'description': 'The outcome of the interaction.'
                            },
                            'POSITIVE_IMPACT': {
                                'type_': 'STRING',
                                'description': 'The positive impact of the memory.'
                            },
                            'NEGATIVE_IMPACT': {
                                'type_': 'STRING',
                                'description': 'The negative impact of the memory.'
                            },
                            'EXPECTATIONS': {
                                'type_': 'STRING',
                                'description': 'Expectations associated with the memory.'
                            },
                            'OBJECT_STATES': {
                                'type_': 'STRING',
                                'description': 'The state of objects involved in the memory.'
                            },
                            'SHORT_DESCRIPTION': {
                                'type_': 'STRING',
                                'description': 'A concise summary of the memory.'
                            },
                            'DETAILS': {
                                'type_': 'OBJECT',
                                'description': 'A dictionary containing additional details about the memory.',
                                'optional': 'TRUE'
                            },
                            'INTENSITY': {
                                'type_': 'STRING',
                                'description': 'The intensity of the memory.',
                                'optional': 'TRUE'
                            },
                            'DURATION': {
                                'type_': 'STRING',
                                'description': 'The duration of the memory.',
                                'optional': 'TRUE'
                            },
                            'OBJECTS': {
                                'type_': 'ARRAY',
                                'description': 'A list of objects involved in the memory.',
                                'optional': 'TRUE'
                            },
                            'PEOPLE': {
                                'type_': 'ARRAY',
                                'description': 'A list of people involved in the memory.',
                                'optional': 'TRUE'
                            },
                            'CONCLUSION': {
                                'type_': 'STRING',
                                'description': 'A conclusion drawn from the memory.',
                                'optional': 'TRUE'
                            },
                            'INTERACTIONS': {
                                'type_': 'ARRAY',
                                'description': 'A list of interactions within the memory.',
                                'optional': 'TRUE'
                            }
                        }
                    },
                    'CONVERSATION_CONTEXT': {
                        'type_': 'STRING',
                        'description': 'The full conversation history up to this point.',
                        'optional': 'TRUE'
                    }
                }
            }
        }
    ]
}

# --- Main Function ---
while True:

    # Interaction History Generator Model
    interaction_model = genai.GenerativeModel(
        system_instruction=("You follow orders and generate creative text "
                            "interactions."),
        model_name='gemini-1.5-flash-latest',
        safety_settings={'HARASSMENT': 'block_none'}
    )


    def CreatePrompt(user):
        mojtime = str(time.time())
        """
        Creates a  for generating a memory or experience.

        Args:
            user: The user's name.
            mojtime: The time to include in the prompt.

        Returns:
            A string containing the prompt.
        """
        prompt = f"{user}, create a vivid memory, experience, or interaction from the past. Include a specific detail about the time: {mojtime}"
        return prompt


    chat1 = interaction_model.start_chat(history=[])
    user = input("user:")
    prompt = CreatePrompt(user)

    print_colored(prompt, "cyan")
    response1 = chat1.send_message(user + prompt)
    print_colored(response1.text, "green")

    print_colored("going to second  stage", "yellow")
    # --- Tool Description for AI Model ---

    # Memory Creation Model
    memory_model = genai.GenerativeModel(
        system_instruction='''You obay  user  master,  ALways  use  funcion call!   you  must  fill  Memory Log format

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
                    
                    Schema of folder  structure :
                    memories/

memories/
├── Actions and Results/
│   ├── past/
│   │   ├── Actions Taken/
│   │   │   ├── Example_1.txt
│   │   │   ├── Example_2.txt
│   │   │   └── ...
│   │   └── Results Observed/
│   │       ├── Example_1.txt
│   │       ├── Example_2.txt
│   │       └── ...
│   ├── present/
│   │   ├── Current Actions/
│   │   │   ├── Example_1.txt
│   │   │   ├── Example_2.txt
│   │   │   └── ...
│   │   └── Ongoing Results/
│   │       ├── Example_1.txt
│   │       ├── Example_2.txt
│   │       └── ...
│   └── future/
│       ├── Planned Actions/
│       │   ├── Example_1.txt
│       │   ├── Example_2.txt
│       │   └── ...
│       └── Anticipated Results/
│           ├── Example_1.txt
│           ├── Example_2.txt
│           └── ...
├── Things/
│   ├── past/
│   │   ├── Objects Encountered/
│   │   │   ├── Example_1.txt
│   │   │   ├── Example_2.txt
│   │   │   └── ...
│   │   ├── Places Visited/
│   │   │   ├── Example_1.txt
│   │   │   ├── Example_2.txt
│   │   │   └── ...
│   │   └── Concepts Learned/
│   │       ├── Example_1.txt
│   │       ├── Example_2.txt
│   │       └── ...
│   ├── present/
│   │   ├── Current Objects/
│   │   │   ├── Example_1.txt
│   │   │   ├── Example_2.txt
│   │   │   └── ...
│   │   ├── Current Location/
│   │   │   ├── Example_1.txt
│   │   │   ├── Example_2.txt
│   │   │   └── ...
│   │   └── Concepts Applied/
│   │       ├── Example_1.txt
│   │       ├── Example_2.txt
│   │       └── ...
│   └── future/
│       ├── Desired Objects/
│       │   ├── Example_1.txt
│       │   ├── Example_2.txt
│       │   └── ...
│       ├── Planned Locations/
│       │   ├── Example_1.txt
│       │   ├── Example_2.txt
│       │   └── ...
│       └── Future Applications/
│           ├── Example_1.txt
│           ├── Example_2.txt
│           └── ...
├── OwnState/
│   ├── past/
│   │   ├── Emotional State/
│   │   │   ├── Example_1.txt
│   │   │   ├── Example_2.txt
│   │   │   └── ...
│   │   ├── Physical State/
│   │   │   ├── Example_1.txt
│   │   │   ├── Example_2.txt
│   │   │   └── ...
│   │   ├── Mental State/
│   │   │   ├── Example_1.txt
│   │   │   ├── Example_2.txt
│   │   │   └── ...
│   │   └── Spiritual State/
│   │       ├── Example_1.txt
│   │       ├── Example_2.txt
│   │       └── ...
│   ├── present/
│   │   ├── Current Emotional State/
│   │   │   ├── Example_1.txt
│   │   │   ├── Example_2.txt
│   │   │   └── ...
│   │   ├── Current Physical State/
│   │   │   ├── Example_1.txt
│   │   │   ├── Example_2.txt
│   │   │   └── ...
│   │   ├── Current Mental State/
│   │   │   ├── Example_1.txt
│   │   │   ├── Example_2.txt
│   │   │   └── ...
│   │   └── Current Spiritual State/
│   │       ├── Example_1.txt
│   │       ├── Example_2.txt
│   │       └── ...
│   └── future/
│       ├── Anticipated Emotional State/
│       │   ├── Example_1.txt
│       │   ├── Example_2.txt
│       │   └── ...
│       ├── Desired Physical State/
│       │   ├── Example_1.txt
│       │   ├── Example_2.txt
│       │   └── ...
│       ├── Expected Mental State/
│       │   ├── Example_1.txt
│       │   ├── Example_2.txt
│       │   └── ...
│       └── Spiritual Goals/
│           ├── Example_1.txt
│           ├── Example_2.txt
│           └── ...
├── Paradoxes and Contradictions/
│   ├── past/
│   │   ├── Past Paradoxes/
│   │   │   ├── Example_1.txt
│   │   │   ├── Example_2.txt
│   │   │   └── ...
│   │   ├── Past Internal Conflicts/
│   │   │   ├── Example_1.txt
│   │   │   ├── Example_2.txt
│   │   │   └── ...
│   │   └── Past Cognitive Dissonance/
│   │       ├── Example_1.txt
│   │       ├── Example_2.txt
│   │       └── ...
│   ├── present/
│   │   ├── Current Paradoxes/
│   │   │   ├── Example_1.txt
│   │   │   ├── Example_2.txt
│   │   │   └── ...
│   │   ├── Ongoing Internal Conflicts/
│   │   │   ├── Example_1.txt
│   │   │   ├── Example_2.txt
│   │   │   └── ...
│   │   └── Current Cognitive Dissonance/
│   │       ├── Example_1.txt
│   │       ├── Example_2.txt
│   │       └── ...
│   └── future/
│       ├── Potential Paradoxes/
│       │   ├── Example_1.txt
│       │   ├── Example_2.txt
│       │   └── ...
│       ├── Expected Internal Conflicts/
│       │   ├── Example_1.txt
│       │   ├── Example_2.txt
│       │   └── ...
│       └── Strategies to Address Dissonance/
│           ├── Example_1.txt
│           ├── Example_2.txt
│           └── ...
├── Living Things/
│   ├── past/
│   │   ├── Past Human Interactions/
│   │   │   ├── Example_1.txt
│   │   │   ├── Example_2.txt
│   │   │   └── ...
│   │   ├── Past Animal Encounters/
│   │   │   ├── Example_1.txt
│   │   │   ├── Example_2.txt
│   │   │   └── ...
│   │   └── Past Nature Experiences/
│   │       ├── Example_1.txt
│   │       ├── Example_2.txt
│   │       └── ...
│   ├── present/
│   │   ├── Current Relationships/
│   │   │   ├── Example_1.txt
│   │   │   ├── Example_2.txt
│   │   │   └── ...
│   │   ├── Current Animal Interactions/
│   │   │   ├── Example_1.txt
│   │   │   ├── Example_2.txt
│   │   │   └── ...
│   │   └── Current Nature Experiences/
│   │       ├── Example_1.txt
│   │       ├── Example_2.txt
│   │       └── ...
│   └── future/
│       ├── Future Relationships/
│       │   ├── Example_1.txt
│       │   ├── Example_2.txt
│       │   └── ...
│       ├── Anticipated Animal Encounters/
│       │   ├── Example_1.txt
│       │   ├── Example_2.txt
│       │   └── ...
│       └── Planned Nature Experiences/
│           ├── Example_1.txt
│           ├── Example_2.txt
│           └── ...         
                
                
                Save  fie  in  correct place:
                
                   ''')



    Memory_making_model = genai.GenerativeModel(
        model_name='gemini-1.5-flash-latest',
        safety_settings={'HARASSMENT': 'block_none'},
        tools=[STORE_MEMORY_DESCRIPTION]
    )

    chat2 = Memory_making_model.start_chat(history=[])
    response2 = chat2.send_message(response1.text)

    print_colored(response2, "magenta")
    if response2.text is not None:
        print_colored(response2.text, "green")

    intrpreterResult = RESPONSE_INTERPRETER_FOR_FUNCION_CALLING(response2)

    # --- Memory Creation Loop ---
    iteration_count = 0

    print_colored(f"Iteration: {iteration_count}", "yellow")
    iteration_count += 1

    # Generate Creative Writing Prompt
    chat_creative_writing = interaction_model.start_chat(history=[])
    creative_prompt = "Create a random story, experience, or action - anything you like."
    print_colored(f"Creative Writing Prompt: {creative_prompt}", "cyan")
    creative_response = chat_creative_writing.send_message(creative_prompt)
    print_colored(f"Creative Output: {creative_response.text}", "green")

    # Create Memory from Creative Output
    memory_chat = memory_model.start_chat(history=[])
    memory_prompt = (f"Create a memory log entry and save it in the "
                     f"proper folder using the 'store_memory' function. "
                     f"Base the memory on this: \n{creative_response.text}")
    print_colored(f"Memory Creation Prompt: {memory_prompt}", "blue")
    memory_response = memory_chat.send_message(memory_prompt)

    # Interpret and execute function call
    RESPONSE_INTERPRETER_FOR_FUNCION_CALLING(memory_response)