import sys
import time
import datetime
import re
import os
from turtle import pd

import google.generativeai as genai
from termcolor import colored, cprint

genai.configure(api_key='AIzaSyDB4T_w4yat1SUGcP5zLl0x94I9Emb6-kY')
import time
import datetime
import re
import os
import google.generativeai as genai
from termcolor import colored, cprint
import datetime

timestamp = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')



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


# --- Function to Create File Structure ---
def create_file_structure():
    """Creates the file structure for storing memories."""
    for category in categories:
        for time_period in ["past", "present", "future"]:
            for subcategory in categories[category][time_period]:
                folder_path = os.path.join("memories", category, time_period, subcategory)
                os.makedirs(folder_path, exist_ok=True)


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


create_file_structure()
print_colored("Generated Memory Folders", "green")


# Define the `store_memory` function here
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


ALLOWED_FUNCTIONS = {
    "store_memory": store_memory,
    # Add more functions here as needed
}


def RESPONSE_INTERPRETER_FOR_FUNCION_CALLING(response):
    """Interprets the model's response, extracts function details, and executes the appropriate function."""
    global store_memory
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

                if function_to_call := ALLOWED_FUNCTIONS.get(function_name):  # Safe function lookup
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


STORE_MEMORY_DESCRIPTION = [

    {
        'name': 'store_memory',
        'description': 'Stores a memory log entry in a file within a hierarchical folder structure. '
        ,
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

from datetime import datetime
import os


import os
from datetime import datetime

def store_conversation_frame(user_input="", ai_response="",
                             ai_response_summary="", session_name="default_session",
                             path="conversation_logs",
                             memory_frame_number=None, edit_number=0):
    """Stores conversation data with enhanced file naming and timestamps.

    Args:
        user_input (str): The user's input.
        ai_response (str): The AI's response.
        ai_response_summary (str): A summary of the AI's response.
        session_name (str): Unique identifier for the conversation.
        path (str): Base directory for storing logs.
        memory_frame_number (int): Frame number. Auto-increments if None.
        edit_number (int): Number of edits to this frame.
    """

    separator = "######$######"
    os.makedirs(path, exist_ok=True)

    # --- Enhanced File Naming ---
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    filename = f"MemoryFrame_{session_name}_{timestamp}.txt"
    filepath = os.path.join(path, filename)

    # --- Memory Frame Numbering ---
    if memory_frame_number is None:
        memory_frame_number = 1

    # --- Frame Data ---
    frame_data = {
        "MEMORY_FRAME_NUMBER": memory_frame_number,
        "EDIT_NUMBER": edit_number,
        "TIMESTAMP": timestamp,
        "USER_INPUT": user_input,
        "AI_RESPONSE": ai_response,
        "AI_RESPONSE_SUMMARY": ai_response_summary
    }

    # --- Construct Content with Readable Timestamps ---
    readable_timestamp = datetime.now().strftime('%A, %B %d, %Y - %H:%M:%S') #day month date year - hour minute second
    frame_content = f"{separator} Memory Frame {memory_frame_number}, Edit {edit_number} - {readable_timestamp} {separator}\n"
    for key, value in frame_data.items():
        frame_content += f"{key}: {value}\n"  # Improved formatting
    frame_content += f"{separator} Memory Frame End {memory_frame_number}, Edit {edit_number} {separator}\n\n" #double /n for readability

    # --- Write to File ---
    with open(filepath, 'a', encoding='utf-8') as f:
        f.write(frame_content)

    print(f"Memory frame saved in: {filepath}")







def categorize_memory(summary, categories):
    """Categorizes a memory frame based on keywords in the summary."""
    # *** Start with Simple Keyword Matching (Improve Later) ***
    for category, subcategories in categories.items():
        for time_period, keyword_list in subcategories.items():
            for keyword in keyword_list:
                if re.search(rf"\b{keyword}\b", summary, re.IGNORECASE):
                    return category, time_period, keyword

    return "uncategorized", "unknown", "unknown"  # Default if no match


while True:
    user = input("enter input")
    interaction_model = genai.GenerativeModel(
        system_instruction=("You follow orders and generate creative text , "
                            "interactions."),
        model_name='gemini-1.5-flash-latest',
        safety_settings={'HARASSMENT': 'block_none'})
    chat1 = interaction_model.start_chat(history=[])
    prompt = f"create   {user}"
    print(f"{prompt}")
    response1 = chat1.send_message(prompt)
    print_colored(response1.text, "green")
    chat1.history = []

    ###########################################################################################
    memory_model = genai.GenerativeModel(
        model_name='gemini-1.5-flash-latest',
        safety_settings={'HARASSMENT': 'block_none'},
        system_instruction="""You are a sophisticated AI assistant helping to organize memories. 
        Analyze and summarize the above user-AI conversation, focusing on elements that would be most useful for storing and retrieving this memory later. Don't hallucinate.""",
    )

    # Generate Creative MemoryLog FunctionCall
    chat_2 = interaction_model.start_chat(history=[])
    json_schema_example = """
    {
      "concise_summary": "Your concise summary of the conversation goes here.",
      "main_topic": "The central theme or subject of the conversation.",
      "keywords": ["keyword1", "keyword2", "keyword3", ...], 
      "entities": ["entity1", "entity2", ...], 
      "actions": ["action1", "action2", ...], 
      "category": "The category of the memory", 
      "subcategory": "The subcategory of the memory",
      "memory_about": "A brief description of what the memory is about", 
      "interaction_type": "Describe the type of interaction that occurred in this conversation.",
      "positive_impact": "What were the positive outcomes or benefits of this conversation?", 
      "negative_impact":  "Were there any negative outcomes or drawbacks discussed?", 
      "expectations": "What were the user's expectations before the conversation?",
      "object_states": "Describe the objects or locations involved.",
      "short_description": "An even briefer summary", 
      "details": {}, // Optional additional details as key-value pairs
      "facts": ["fact1", "fact2", ...],
      "contradictions_paradoxes": ["contradiction1", "paradox2", ...],
      "strength_of_experience": "A description of the intensity or significance of this conversation for the user.",
      "personal_information": "Any relevant personal details",
      "observed_interactions": ["interaction1", "interaction2", ...],
      "people": ["person1", "person2", ...],
      "objects": ["object1", "object2", ...],
      "animals": ["animal1", "animal2", ...],
      "obtained_knowledge": "What new knowledge or insights were gained from this conversation?",
      "scientific_data": ["data_point1", "data_point2", ...],
      "tags": ["tag1", "tag2", ...] // For additional retrieval 
    }
    """
    CreateMemoryPrompt = f'''User: {user}
                                  AI: {response1.text}

                                  You are a sophisticated AI assistant helping to organize memories. 
    Analyze and summarize the above user-AI conversation, focusing on elements that would be most useful for storing and retrieving this memory later. Don't hallucinate.

    Specifically, provide the following information in a structured format using JSON:
    {json_schema_example}

   '''

    print(CreateMemoryPrompt)
    response2 = chat_2.send_message(CreateMemoryPrompt)
    print("---------------------------------------------------------------------------------------------------------")
    print(response2.text)

    RESPONSE_INTERPRETER_FOR_FUNCION_CALLING(
        response2)  # check and fix inconsistencies: for example   Personal  is on red

    store_conversation_frame(user_input=user, ai_response=response1.text, ai_response_summary=response2.text)