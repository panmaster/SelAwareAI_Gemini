import sys
import time
import datetime
import re
import os
from turtle import pd

import google.generativeai as genai
from termcolor import colored, cprint

genai.configure(api_key='AIzaSyDEa1BAKI4ybj4N8Xloo4XY5uW5X62e-lw')
import time
import datetime
import re
import os
import google.generativeai as genai
from termcolor import colored, cprint
import datetime
import os
from datetime import datetime
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


create_file_structure()
print_colored("Generated Memory Folders", "green")



def store_memory(memory_data, category, time_period, subcategory):
    """Stores memory data into the appropriate folder."""
    memory_frame_number = memory_data.get('MEMORY_FRAME_NUMBER', 1)  # Default to 1 if not provided
    edit_number = memory_data.get('EDIT_NUMBER', 0)  # Default to 0 if not provided
    timestamp = memory_data.get('TIMESTAMP', datetime.datetime.now().strftime('%Y%m%d_%H%M%S'))

    folder_path = os.path.join("memories", category, time_period, subcategory)
    filename = f"MemoryFrame_{memory_frame_number}_{edit_number}_{timestamp}.txt"
    filepath = os.path.join(folder_path, filename)

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(str(memory_data))
    print_colored(f"Memory stored in: {filepath}", "green")


ALLOWED_FUNCTIONS = {
    "store_memory": store_memory,
    # Add more functions here as needed
}


def RESPONSE_INTERPRETER_FOR_FUNCION_CALLING(response):
    # ... your existing code ...

    if response.candidates:
        for part in response.candidates[0].content.parts:
            if hasattr(part, 'function_call'):
                function_call = part.function_call
                function_name = function_call.name
                function_args = function_call.args

                # **Important Change:** Handle None case
                if function_args is not None:
                    # ... your existing code ...

                else:
                    print_colored(f"Warning: Function call arguments are missing.", "red")

    return Multiple_ResultsOfFunctions_From_interpreter


STORE_MEMORY_DESCRIPTION = [

    {
    }
]

from datetime import datetime
import os




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
    readable_timestamp = datetime.now().strftime('%A, %B %d, %Y - %H:%M:%S')  # day month date year - hour minute second
    frame_content = f"{separator} Memory Frame {memory_frame_number}, Edit {edit_number} - {readable_timestamp} {separator}\n"
    for key, value in frame_data.items():
        frame_content += f"{key}: {value}\n"  # Improved formatting
    frame_content += f"{separator} Memory Frame End {memory_frame_number}, Edit {edit_number} {separator}\n\n"  # double /n for readability

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

    results = RESPONSE_INTERPRETER_FOR_FUNCION_CALLING(response2)
    for result in results:
        print(result)

    # --- Categorize and Store the Memory ---
    memory_data = response2.candidates[0].content.parts[0].function_call.args
    category, time_period, subcategory = categorize_memory(memory_data['concise_summary'], categories)
    print_colored(f"Categorized as: {category}, {time_period}, {subcategory}", "cyan")

    store_memory(memory_data, category, time_period, subcategory)
    store_conversation_frame(user_input=user, ai_response=response1.text, ai_response_summary=response2.text)