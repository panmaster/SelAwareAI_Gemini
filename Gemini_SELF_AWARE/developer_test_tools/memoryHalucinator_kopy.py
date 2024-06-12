import sys
import time
import datetime
import re
import os
from datetime import datetime

import google.generativeai as genai
from termcolor import colored, cprint
import os
import pickle

genai.configure(api_key='AIzaSyDB4T_w4yat1SUGcP5zLl0x94I9Emb6-kY')

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


def categorize_memory(summary, categories):
    """Categorizes a memory frame based on keywords in the summary."""
    for category, subcategories in categories.items():
        for time_period, keyword_list in subcategories.items():
            for keyword in keyword_list:
                if re.search(rf"\b{keyword}\b", summary, re.IGNORECASE):
                    return category, time_period, keyword

    return "uncategorized", "unknown", "unknown"


# --- Function to Search for Memories ---
def search_memories(query, category=None, time_period=None):
    """Searches for memories based on the given criteria."""
    matching_memories = []
    for root, _, files in os.walk("memories"):
        for file in files:
            if file.endswith(".txt"):
                filepath = os.path.join(root, file)
                # Check if the category and time_period match (if provided)
                if category and category not in filepath:
                    continue
                if time_period and time_period not in filepath:
                    continue
                # Search within the file content
                with open(filepath, 'r', encoding='utf-8') as f:
                    content = f.read()
                    if query.lower() in content.lower():
                        matching_memories.append(filepath)
    return matching_memories


def response_interpreter_for_function_calling(response):
    """Interprets the AI's response and executes function calls
       (excluding memory storage).
    """
    outcome = []
    if response.candidates:
        for part in response.candidates[0].content.parts:
            if hasattr(part, 'function_call'):
                function_call = part.function_call
                function_name = function_call.name
                function_args = function_call.args

                if function_name in FUNCTION_MAPPING:
                    function_to_call = FUNCTION_MAPPING[function_name]
                    if function_args is not None:
                        try:
                            outcome = function_to_call(**function_args)
                        except Exception as e:
                            print_colored(
                                f"Error executing function {function_name}: {e}",
                                "blue"
                            )
                    else:
                        print_colored(
                            "Warning: Function call arguments are missing.", "red"
                        )
                else:
                    print(response)
                    print_colored(

                        f"Error: Unknown function: {function_name}", "red"
                    )
            else:
                print_colored(
                    "No function call found in the response.", "blue"
                )
    if outcome is None:
        outcome = ""
    return outcome


# You can add other useful functions here
FUNCTION_MAPPING = {
    # Example:
    # "play_music": play_music,
}


def STORE_MEMORY_Frame(current_time, user_input, ai_response,  response2, memory_data):
    """Stores both structured memory data and the conversation frame."""

    memory_frame_number = memory_data.get('MEMORY_FRAME_NUMBER', 1)
    edit_number = memory_data.get('EDIT_NUMBER', 0)
    timestamp = current_time

    def determine_storage_location(memory_data, categories):
        """Determines the optimal storage location for a memory frame."""
        summary_data = memory_data['AI_RESPONSE_SUMMARY']

        # --- 1. Extract Relevant Information ---

        concise_summary = summary_data.get('concise_summary', "")
        main_topic = summary_data.get('main_topic', "")
        keywords = summary_data.get('keywords', [])
        entities = summary_data.get('entities', [])
        actions = summary_data.get('actions', [])

        # --- 2. Determine Best Category and Time Period ---

        best_category = None
        best_time_period = None
        best_subcategory = None

        # (a) Start with Direct Matches (Category and Subcategory)
        for category, subcategories in categories.items():
            for time_period, subcategory_list in subcategories.items():
                for subcategory in subcategory_list:
                    if (
                            category.lower() in concise_summary.lower() or
                            subcategory.lower() in concise_summary.lower()
                    ):
                        best_category = category
                        best_time_period = time_period
                        best_subcategory = subcategory
                        break  # Found a direct match, stop searching

        # (b) Use Keywords and Entities for Matching (if no direct match)
        if best_category is None:
            for category, subcategories in categories.items():
                for time_period, subcategory_list in subcategories.items():
                    for keyword in keywords + entities:  # Combine lists
                        if keyword.lower() in subcategory_list:
                            best_category = category
                            best_time_period = time_period
                            best_subcategory = keyword.lower()
                            break

        # (c) Fallback: Uncategorized (if no match found)
        if best_category is None:
            best_category = "Uncategorized"
            best_time_period = "unknown"
            best_subcategory = "unknown"

        # --- 3. Check for Existing Subcategory or Create New ---

        if best_subcategory not in categories[best_category][best_time_period]:
            categories[best_category][best_time_period].append(best_subcategory)
            # ... (Create the new folder in your file system as well)
            print_colored(
                f"Created new subcategory: '{best_subcategory}' in "
                f"'{best_category}/{best_time_period}'",
                "green"
            )

        # --- 4. Determine Filepath ---

        folder_path = os.path.join(
            "memories", best_category, best_time_period, best_subcategory
        )
        os.makedirs(folder_path, exist_ok=True)  # Ensure the folder exists

        filename = f"MemoryFrame_{memory_frame_number}_{edit_number}_{timestamp}.txt"
        filepath = os.path.join(folder_path, filename)

        return filepath, best_category, best_time_period, best_subcategory

    # --- Store Memory Data ---
    filepath, best_category, best_time_period, best_subcategory = determine_storage_location(memory_data, categories)
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(str(memory_data))
    print_colored(f"Memory stored in: {filepath}", "green")

    # --- Store Conversation Frame ---
    separator = "######$######"
    os.makedirs("memories/conversation_logs", exist_ok=True)

    conversation_filename = f"MemoryFrame_{timestamp}.txt"
    conversation_filepath = os.path.join("memories/conversation_logs",
                                         conversation_filename)

    readable_timestamp = datetime.now().strftime('%A, %B %d, %Y - %H:%M:%S')
    frame_content = f"{separator} Memory Frame {memory_frame_number}, Edit {edit_number} - {readable_timestamp} {separator}\n"
    frame_content += f"USER_INPUT: {user_input}\n"
    frame_content += f"AI_RESPONSE: {ai_response}\n"
    frame_content += f"AI_RESPONSE_SUMMARY: {str(memory_data)}\n"
    frame_content += f"{separator} Memory Frame End {memory_frame_number}, Edit {edit_number} {separator}\n\n"

    with open(conversation_filepath, 'a', encoding='utf-8') as f:
        f.write(frame_content)

    print(f"Memory frame saved in: {conversation_filepath}")

    # --- Update Memory Frame Log ---
    os.makedirs("memory_logs", exist_ok=True)
    memory_log_filepath = os.path.join("memory_logs", "MemoryFrames_log.txt")
    script_path = os.path.abspath(os.path.dirname(__file__))

    with open(memory_log_filepath, 'a', encoding='utf-8') as f:
        f.write(
            f"MemoryFrame: {memory_frame_number}, Edit: {edit_number}, Type: Text, path: {filepath}, time: {timestamp}, session: {memory_frame_number}_{edit_number}\n")

    print(f"Memory frame log updated: {memory_log_filepath}")


# --- Main Loop ---
memory_data = {
    'MEMORY_FRAME_NUMBER': 1,  # Initialize memory frame number
    'EDIT_NUMBER': 0  # Initialize edit number
}
while True:
    try:
        user_input = input("Enter input: ")

        interaction_model = genai.GenerativeModel(
            model_name='gemini-1.5-flash-latest',
            safety_settings={'HARASSMENT': 'block_none'},
            system_instruction='You follow orders and generate creative text interactions'
        )

        current_time = datetime.now().strftime('%Y%m%d_%H%M%S')  # Use current_time
        chat1 = interaction_model.start_chat(history=[])
        prompt = f"currentTime:  {current_time}  create {user_input} "
        print(f"Prompt:  {prompt}")
        response1 = chat1.send_message(prompt)
        try:
            print_colored(f"AI Response: {response1.text}", "green")
        except Exception as e:
            print(e)

        # --- Memory Processing with Gemini ---
        memory_model = genai.GenerativeModel(
            model_name='gemini-1.5-flash-latest',
            safety_settings={'HARASSMENT': 'block_none'},
            system_instruction="""You are a sophisticated AI assistant helping to organize memories. 
                    Analyze and summarize the above user-AI conversation, focusing on elements that would be most useful for storing and retrieving this memory later. Don't hallucinate.
                    use provided schema  for  response
                    Specifically, provide the following information in a structured format using JSON:
                    """,

        )

        schema_for_chat2 = """    
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

        chat_2 = memory_model.start_chat(history=[])
        create_memory_prompt = f"""User: {user_input}
                                    AI: {response1.text}
                                    Schema:
                                    {schema_for_chat2}"""

        print(create_memory_prompt)

        response2 = chat_2.send_message(create_memory_prompt)
        print("-----------------------------------------------------------------------------------")
        print(f"Memory Data: {response2.text}")

        # --- Function Execution ---
        response_interpreter_for_function_calling(response2)

        STORE_MEMORY_Frame(
            current_time,  # Pass current_time as the first argument
            user_input,
            response1.text,
            response2.text,
            memory_data
        )

    except Exception as e:
        print_colored(f"Error in the main loop: {e}", "red")