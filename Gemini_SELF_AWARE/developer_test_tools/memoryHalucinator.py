import time
import datetime
import re
import os
import google.generativeai as genai
from termcolor import colored, cprint
genai.configure(api_key='AIzaSyDEa1BAKI4ybj4N8Xloo4XY5uW5X62e-lw')
import time
import datetime
import re
import os
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




def RESPONSE_INTERPRETER_FOR_FUNCION_CALLING(response):
    """Interprets the model's response, extracts function details, and executes the appropriate function."""
    global  store_memory
    print_colored(f"---------------RESPONSE_INTERPRETER_FOR_FUNCION_CALLING START----------------------", "yellow")
    Multiple_ResultsOfFunctions_From_interpreter = []

    if response.candidates:
        for part in response.candidates[0].content.parts:
            if hasattr(part, 'function_call'):
                function_call = part.function_call
                function_name = function_call.name
                function_args = function_call.args

                # Get the function from the tool manage
                function_to_call = globals().get(store_memory)

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

                            },
                            'INTENSITY': {
                                'type_': 'STRING',
                                'description': 'The intensity of the memory.',

                            },
                            'DURATION': {
                                'type_': 'STRING',
                                'description': 'The duration of the memory.',

                            },
                            'OBJECTS': {
                                'type_': 'ARRAY',
                                'description': 'A list of objects involved in the memory.',

                            },
                            'PEOPLE': {
                                'type_': 'ARRAY',
                                'description': 'A list of people involved in the memory.',

                            },
                            'CONCLUSION': {
                                'type_': 'STRING',
                                'description': 'A conclusion drawn from the memory.',

                            },
                            'INTERACTIONS': {
                                'type_': 'ARRAY',
                                'description': 'A list of interactions within the memory.',

                            }
                        }
                    },
                    'CONVERSATION_CONTEXT': {
                        'type_': 'STRING',
                        'description': 'The full conversation history up to this point.',

                    }
                }
            }
        }
    ]
}

# --- Main Function ---
while True:


    interaction_model = genai.GenerativeModel(
        system_instruction=("You follow orders and generate creative text "
                            "interactions."),
        model_name='gemini-1.5-flash-latest',
        safety_settings={'HARASSMENT': 'block_none'})
    chat1 = interaction_model.start_chat(history=[])
    prompt=f"create  story, expiriane, or  actions, some  random  stuff"
    print(f"{prompt}")
    response1 = chat1.send_message(prompt)
    print_colored(response1.text, "green")
    print(response1.text)




    ###########################################################################################
    memory_model = genai.GenerativeModel(
        model_name='gemini-1.5-flash-latest',
        safety_settings={'HARASSMENT': 'block_none'},
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
    │   │   │   
    │   │   └── Results Observed/
    │   │       
    │   ├── present/
    │   │   ├── Current Actions/
    │   │   │   
    │   │   └── Ongoing Results/
    │   │       
    │   └── future/
    │       ├── Planned Actions/
    │       │   
    │       └── Anticipated Results/
    │           
    ├── Things/
    │   ├── past/
    │   │   ├── Objects Encountered/
    │   │   │   
    │   │   ├── Places Visited/
    │   │   │   
    │   │   └── Concepts Learned/
    │   │       
    │   ├── present/
    │   │   ├── Current Objects/
    │   │   │   
    │   │   ├── Current Location/
    │   │   │   
    │   │   └── Concepts Applied/
    │   │       
    │   └── future/
    │       ├── Desired Objects/
    │       │   
    │       ├── Planned Locations/
    │       │   
    │       └── Future Applications/
    │           
    ├── OwnState/
    │   ├── past/
    │   │   ├── Emotional State/
    │   │   │   
    │   │   ├── Physical State/
    │   │   │   
    │   │   ├── Mental State/
    │   │   │   
    │   │   └── Spiritual State/
    │   │       
    │   ├── present/
    │   │   ├── Current Emotional State/
    │   │   │   
    │   │   ├── Current Physical State/
    │   │   │   
    │   │   ├── Current Mental State/
    │   │   │   
    │   │   └── Current Spiritual State/
    │   │       
    │   └── future/
    │       ├── Anticipated Emotional State/
    │       │   
    │       ├── Desired Physical State/
    │       │   
    │       ├── Expected Mental State/
    │       │   
    │       └── Spiritual Goals/
    │           
    ├── Paradoxes and Contradictions/
    │   ├── past/
    │   │   ├── Past Paradoxes/
    │   │   │   
    │   │   ├── Past Internal Conflicts/
    │   │   │   
    │   │   └── Past Cognitive Dissonance/
    │   │       
    │   ├── present/
    │   │   ├── Current Paradoxes/
    │   │   │   
    │   │   ├── Ongoing Internal Conflicts/
    │   │   │   
    │   │   └── Current Cognitive Dissonance/
    │   │       
    │   └── future/
    │       ├── Potential Paradoxes/
    │       │   
    │       ├── Expected Internal Conflicts/
    │       │   
    │       └── Strategies to Address Dissonance/
    │           
    ├── Living Things/
    │   ├── past/
    │   │   ├── Past Human Interactions/
    │   │   │   
    │   │   ├── Past Animal Encounters/
    │   │   │   
    │   │   └── Past Nature Experiences/
    │   │      
    │   ├── present/
    │   │   ├── Current Relationships/
    │   │   │   
    │   │   ├── Current Animal Interactions/
    │   │   │   
    │   │   └── Current Nature Experiences/
    │   │       
    │   └── future/
    │       ├── Future Relationships/
    │       │   
    │       ├── Anticipated Animal Encounters/
    │       │   
    │       └── Planned Nature Experiences/
    │           

                    Save  fie  in  folder/subfolder with correct name:

                      ''',
        tools=[STORE_MEMORY_DESCRIPTION],)



    # Generate Creative MemoryLog FunctionCall
    chat_2 = interaction_model.start_chat(history=[])
    CreateMemoryPrompt = (f""""Create a memory log entry and save it in the 
                               proper folder using the 'store_memory' function call 
                               Base the memory on this: \n {response1.text}""")
    response2=chat_2.send_message(CreateMemoryPrompt)
    print(response2)

    RESPONSE_INTERPRETER_FOR_FUNCION_CALLING(response2)  # check and fix inconsistencies: for example   Personal  is on red