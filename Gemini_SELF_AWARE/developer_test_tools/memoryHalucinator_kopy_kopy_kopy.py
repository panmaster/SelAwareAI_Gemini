import sys
import time
import datetime
import re
import os
from datetime import datetime

import google.generativeai as genai
from termcolor import colored, cprint
import pickle

# Configure the API key for Google Generative AI
genai.configure(api_key='AIzaSyAcGOOiy3ChC8BZ6Rczo4k8y2xDhG9G4pQ')

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

categories2 = {
    "Events": {
        "subcategories": ["Past", "Present", "Future"],
        "keywords": ["event", "experience", "occurrence", "incident", "happening", "episode"]
    },
    "Actions": {
        "subcategories": ["Completed", "Ongoing", "Planned"],
        "keywords": ["action", "activity", "task", "goal", "objective", "step", "process"]
    },
    "Thoughts and Emotions": {
        "subcategories": ["Cognitive", "Affective"],
        "keywords": ["thought", "idea", "belief", "realization", "expectation", "emotion", "feeling", "mood", "sentiment"]
    },
    "Knowledge and Learning": {
        "subcategories": ["Acquired", "Applied", "Future Applications"],
        "keywords": ["knowledge", "learning", "understanding", "concept", "skill", "information", "application"]
    },
    "Relationships and Interactions": {
        "subcategories": ["Personal", "Professional", "Social"],
        "keywords": ["relationship", "interaction", "connection", "bond", "association", "encounter", "communication"]
    },
    "Locations and Environments": {
        "subcategories": ["Physical", "Virtual", "Conceptual"],
        "keywords": ["location", "place", "environment", "setting", "context", "situation", "space", "realm"]
    },
    "Objects and Entities": {
        "subcategories": ["Physical", "Digital", "Conceptual"],
        "keywords": ["object", "entity", "item", "thing", "concept", "idea", "construct"]
    },
    "Paradoxes and Conflicts": {
        "subcategories": ["Internal", "External"],
        "keywords": ["paradox", "contradiction", "conflict", "dissonance", "inconsistency", "dilemma", "tension"]
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

def categorize_memory(summary, categories):
    """Categorizes a memory frame based on keywords in the summary."""
    for category, subcategories in categories.items():
        for time_period, keyword_list in subcategories.items():
            for keyword in keyword_list:
                if re.search(rf"\b{keyword}\b", summary, re.IGNORECASE):
                    return category, time_period, keyword

    return "uncategorized", "unknown", "unknown"

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
    try:
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
    except Exception as e:
        print(e)
    if outcome is None:
        outcome = ""
    return outcome

# You can add other useful functions here
FUNCTION_MAPPING = {
    # Example:
    # "play_music": play_music,
}

def STORE_MEMORY_Frame(current_time, user_input, ai_response, ai_response2, memory_data):
    """Stores both structured memory data and the conversation frame."""

    memory_frame_number = memory_data.get('MEMORY_FRAME_NUMBER', 1)
    edit_number = memory_data.get('EDIT_NUMBER', 0)

    # Format timestamp in YYYY-MM-DD_HH-MM-SS
    timestamp_format = "%Y-%m-%d_%H-%M-%S"
    timestamp = current_time.strftime(timestamp_format)

    script_path = os.path.abspath(os.path.dirname(__file__))  # Get script directory

    # --- Store Memory Data ---
    os.makedirs(os.path.join(script_path, "memories"), exist_ok=True)
    filepath = os.path.join(script_path, "memories", f"MemoryFrame_{memory_frame_number}_{edit_number}_{timestamp}.txt")

    # Construct the memory frame content as a string
    memory_frame_content = f"MEMORY_FRAME_NUMBER: {memory_frame_number}\n"
    memory_frame_content += f"EDIT_NUMBER: {edit_number}\n"
    memory_frame_content += f"TIMESTAMP: {timestamp}\n"
    memory_frame_content += f"USER_INPUT: {user_input}\n"
    memory_frame_content += f"AI_RESPONSE: {ai_response}\n"
    memory_frame_content += f"AI_RESPONSE_SUMMARY: {ai_response2}\n"

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(memory_frame_content)
    print_colored(f"Memory stored in: {filepath}", "green")

    # --- Store Conversation Frame ---
    separator = "######$######"
    os.makedirs(os.path.join(script_path, "conversation_logs"), exist_ok=True)

    conversation_filename = f"MemoryFrame_{timestamp}.txt"
    conversation_filepath = os.path.join(script_path, "conversation_logs", conversation_filename)

    # Format timestamp for conversation log
    readable_timestamp = current_time.strftime('%Y-%m-%d %H:%M:%S')
    frame_content = f"{separator} Memory Frame {memory_frame_number}, Edit {edit_number} - {readable_timestamp} {separator}\n"
    frame_content += f"USER_INPUT: {user_input}\n"
    frame_content += f"AI_RESPONSE: {ai_response}\n"
    frame_content += f"AI_RESPONSE_SUMMARY: {ai_response2}\n"  # Assuming ai_response2 holds the JSON data
    frame_content += f"{separator} Memory Frame End {memory_frame_number}, Edit {edit_number} {separator}\n\n"

    with open(conversation_filepath, 'a', encoding='utf-8') as f:
        f.write(frame_content)

    print(f"Memory frame saved in: {conversation_filepath}")

    # --- Update Memory Frame Log ---
    os.makedirs(os.path.join(script_path, "memory_logs"), exist_ok=True)
    memory_log_filepath = os.path.join(script_path, "memory_logs", "MemoryFrames_log.txt")

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

        current_time = datetime.now()

        # Format timestamp outside the prompt
        formatted_timestamp = current_time.strftime('%Y-%m-%d_%H-%M-%S')

        chat1 = interaction_model.start_chat(history=[])
        prompt = f"currentTime: {formatted_timestamp} create {user_input}"
        print(f"Prompt: {prompt}")
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
                Use the provided schema for response.
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
