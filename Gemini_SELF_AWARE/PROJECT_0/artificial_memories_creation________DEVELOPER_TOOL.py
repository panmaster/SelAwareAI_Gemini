import google.generativeai as genai
import os
import json
import re
from datetime import datetime
from collections import defaultdict
import time
import random
import pathlib



genai.configure(api_key='AIzaSyDRJJmMsB7WQXQ8P0mKTCHf9VIx5uprTw8')  # Replace with your actual API key
BLACK = "\033[30m"
RED = "\033[31m"
GREEN = "\033[32m"
YELLOW = "\033[33m"
BLUE = "\033[34m"
MAGENTA = "\033[35m"
CYAN = "\033[36m"
WHITE = "\033[37m"
RESET = "\033[0m"


def sanitize_href(href, memories_folder_path):
    """Sanitizes a given href string by replacing spaces with %20."""
    href = href.replace(" ", "%20")  # Replace spaces with %20
    return href

def update_html_logs(memory_frame_number, proposed_name, timestamp, memory_frame_paths, memories_folder_path):
    """Updates the HTML log file with CORRECT absolute paths for href links."""
    try:
        log_file_path = os.path.join(memories_folder_path, 'Memory_logs.html')

        if not os.path.exists(log_file_path):
            with open(log_file_path, 'w') as log_file:
                log_file.write("""
                   <!DOCTYPE html>
                   <html>
                   <head>
                       <title>Memory Logs</title>
                   </head>
                   <body>
                       <h1>Memory Logs</h1>
                       <ul>
                   """)

        html_insertion = f"""
               <li><h2>Memory Frame {memory_frame_number:05d} - {proposed_name} ({timestamp})</h2></li>
               <ul>
           """

        for memory_frame_path in memory_frame_paths:
            # Calculate the relative path from the "memory" folder
            relative_path = os.path.relpath(memory_frame_path, memories_folder_path)

            # Construct the href using the relative path
            href = f'memory/{relative_path}'  # Correctly create the relative path

            html_insertion += f"""
                       <li><a href='{href}'>{os.path.basename(href)}</a></li> 
                   """

        html_insertion += "</ul>"

        with open(log_file_path, 'a') as log_file:
            log_file.write(html_insertion)

        print(f"{GREEN}HTML logs updated successfully.{RESET}")
    except Exception as e:
        print(f"Error updating HTML logs: {e}")




# --- Global Variables ---
MEMORY_FRAME_NUMBER = 1
EDIT_NUMBER = 0
counter = 0
TIMESTAMP_FORMAT = '%Y-%m-%d_%H-%M'
print(counter)


def Get_path_of_memories_folder():
    """Returns the absolute path to the 'memory' folder."""
    current = pathlib.Path.cwd()
    memories_path = current / "memory"
    return memories_path.absolute()


path_o_Memories_folder = Get_path_of_memories_folder()

# Example usage:
memories_folder = Get_path_of_memories_folder()
print(f"Memories folder path: {memories_folder}")











categories = [
  "animals"
]
def process_user_input():
    global counter
    global categories
    print(f"CREATION OF A  MEMORY = loop  number  {counter}")

    counter = counter + 1
    random_number = random.randint(1, 100)
    randomiser = random_number * random_number - counter + counter * counter
    randomiser_str = str(randomiser)

    prompt_construction = f"{counter} Important  information and  description  of {categories}    randomiser={randomiser_str} random  animal: dont aks  questions, choose only 1  animal "

    user_input = prompt_construction

    return user_input














def call_interaction_model(user_input, timestamp):
    print(f"\n{CYAN}--- Calling Interaction Model ---{RESET}")
    try:
        interaction_model = genai.GenerativeModel(
            model_name='gemini-1.5-flash-latest',
            safety_settings={'HARASSMENT': 'block_none'},
            system_instruction=""" you fallow user  orders"""
        )
        chat = interaction_model.start_chat(history=[])
        response = chat.send_message(f"currentTime: {timestamp} create {user_input}")
        print(f"AI Response: {response.text}")
        return response
    except Exception as e:
        print(f"Error in Interaction Model: {e}")
        return None


def call_memory_model(user_input, response1_text):
    print(f"\n{CYAN}--- Calling Memory Model ---{RESET}")
    try:
        memory_model = genai.GenerativeModel(
            model_name='gemini-1.5-flash-latest',
            safety_settings={'HARASSMENT': 'block_none'},
            system_instruction="""You are a sophisticated AI assistant helping to organize memory. 
            Analyze and summarize the above user-AI conversation, focusing on elements that would be most useful for storing and retrieving this memory later. Don't hallucinate. 
            Use the provided JSON schema for your response and fill in all fields with relevant information.
            You can omit entries if they don't seem appropriate for memory storage and would be empty.
            Never omit the "memory_folders_storage" entry.

            **JSON Schema:**

            ```json
            {
              "metadata": {
                "creation_date": "", 
                "source": "", 
                "author": "" 
              },
              "type": "conversation", // OR "technical_concept" 
              "engine": {
                "main_topic": "", 
                "category": "", 
                "subcategory": "", 
                "memory_about": "" 
              },
              "summary": {
                "concise_summary": "", 
                "description": "" 
              },
              "content": {
                "keywords": [], 
                "entities": [], 
                "tags": [], 
                "observations": [], 
                "facts": [], 
                "contradictions": [], 
                "paradoxes": [], 
                "scientific_data": [], 
                "visualizations": [] 
              },
              "interaction": {
                "interaction_type": [], 
                "people": [], 
                "objects": [], 
                "animals": [], 
                "actions": [], 
                "observed_interactions": [] 
              },
              "impact": {
                "obtained_knowledge": "", 
                "positive_impact": "", 
                "negative_impact": "", 
                "expectations": "", 
                "strength_of_experience": "" 
              },
              "importance": {
                "reason": "", 
                "potential_uses": [], 
                "importance_level": "0-100" 
              },
              "technical_details": {
                "problem_solved": "", 
                "concept_definition": "", 
                "implementation_steps": [], 
                "tools_and_technologies": [], 
                "example_projects": [], 
                "best_practices": [], 
                "common_challenges": [], 
                "debugging_tips": [], 
                "related_concepts": [], 
                "resources": [], 
                "code_examples": [] 
              },
              "storage": {
                "storage_method": "", 
                "location": "", 
                "memory_folders_storage": [
                  {
                    "folder_path": "", 
                    "probability": 0  
                  }
                ],
                "strength_of_matching_memory_to_given_folder": [] 
              },
              "naming_suggestion": {
                "memory_frame_name": "Give  Same  meaning full name for  Memory File",
                "explanation": "" 
              }
            }
            ```

            **Memory Storage Suggestions:**
            Provide your suggestions for where this memory frame should be stored using the following format within the "memory_folders_storage" field:

            * **"folder_path":** The relative path for storing the memory frame (use '/' as the path separator).
            * **"probability":** The strength of probability (from 0 to 10) that the memory frame should be stored in the suggested folder. Use a scale from 0 (least likely) to 10 (most likely) to express your confidence. 
        """
        )
        chat = memory_model.start_chat(history=[])
        create_memory_prompt = f"User: {user_input}\nAI: {response1_text}"
        response = chat.send_message(create_memory_prompt)
        print(f"Memory Model Response:\n{response.text}")
        return response
    except Exception as e:
        print(f"Error in Memory Model: {e}")
        return None


def extract_entries_smart(response_message):
    """
    Extracts structured entries from the AI response containing JSON data.

    Args:
        response_message (str): The raw text response from the AI model.

    Returns:
        list: A list of dictionaries, where each dictionary represents an extracted entry.
              Returns an empty list if no JSON data is found.
    """
    print("\n--- Extracting Structured Entries ---")
    entries = []
    json_match = re.search(r"```json\n(.*?)\n```", response_message, re.DOTALL)
    if json_match:
        print("Found JSON data in the response.")
        try:
            json_data = json_match.group(1)
            print("Parsing JSON data...")
            response_data = json.loads(json_data)
            print("JSON data parsed successfully.")

            # --- Correctly populate the 'entry' dictionary ---
            entry = defaultdict(lambda: defaultdict(list))
            for key, value in response_data.items():
                if isinstance(value, dict):  # Handle nested dictionaries
                    for sub_key, sub_value in value.items():
                        entry[key][sub_key] = sub_value
                else:
                    entry[key] = value

            print("Handling 'storage' field...")
            entry["storage"] = {
                "storage_method": "",
                "location": "",
                "memory_folders_storage": response_data.get("storage", {}).get("memory_folders_storage", []),
                "strength_of_matching_memory_to_given_folder": []
            }
            print("Validating probabilities in 'memory_folders_storage'...")
            for folder_info in entry["storage"]["memory_folders_storage"]:
                try:
                    probability = folder_info.get("probability")
                    if probability is not None and isinstance(probability, int) and not 0 <= probability <= 10:
                        print(
                            f"Warning: Invalid probability value '{probability}' found in memory_folders_storage. Valid range is 0 to 10."
                        )
                except Exception as e:
                    print(f"Error validating probability in 'memory_folders_storage': {e}")
            print(f"Appending extracted entry: {dict(entry)}")
            entries.append(dict(entry))
        except json.JSONDecodeError:
            print("Error: Invalid JSON in the AI response.")
        except Exception as e:
            print(f"Error extracting entry: {e}")
    return entries





def store_memory_frame(user_input, response1_text, response2_text, memory_data):
    """Saves memory frame data and updates the HTML log."""
    global MEMORY_FRAME_NUMBER, EDIT_NUMBER

    timestamp = datetime.now().strftime(TIMESTAMP_FORMAT)
    proposed_name = memory_data.get("naming_suggestion", {}).get("memory_frame_name", "UnnamedMemory")
    importance = memory_data.get("importance", {}).get("importance_level", "UnknownImportance")

    print(f"\n{YELLOW}--- Storing Memory Frame: {proposed_name} ---{RESET}")

    # Load Connection Map
    connection_map = load_connection_map()

    memory_frame_paths = []
    for folder_info in memory_data.get("storage", {}).get("memory_folders_storage", []):
        folder_path = folder_info.get("folder_path", "")
        probability = folder_info.get("probability", 0)

        target_folder_path = connection_map.get(folder_path, os.path.join(
            os.path.abspath(os.path.dirname(__file__)), "memory", "NewGeneratedbyAI", folder_path
        ))
        # Normalize the target_folder_path:
        target_folder_path = target_folder_path.replace("\\", "/")
        os.makedirs(target_folder_path, exist_ok=True)

        memory_frame_name = (
            f"MemoryFrame_{MEMORY_FRAME_NUMBER:05d}_"
            f"{timestamp}_probabilityOfMatching_{probability}_"
            f"importance_{importance}__{proposed_name}.json"
        )
        memory_frame_path = os.path.join(target_folder_path, memory_frame_name)
        memory_frame_paths.append(memory_frame_path)

        memory_frame_data = {
            "input": user_input,
            "response1": response1_text,
            "response2": response2_text,
            "memory_data": memory_data,
            "timestamp": timestamp,
            "edit_number": EDIT_NUMBER
        }

        try:
            with open(memory_frame_path, 'w') as file:
                json.dump(memory_frame_data, file, indent=4)
            print(f"{GREEN}Memory frame saved successfully at: {memory_frame_path}{RESET}")
        except Exception as e:
            print(f"{RED}Error saving memory frame: {e}{RESET}")

    # Get the full memory folder path
    memories_folder_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "memory"))

    update_html_logs(MEMORY_FRAME_NUMBER, proposed_name, timestamp, memory_frame_paths, memories_folder_path)
    MEMORY_FRAME_NUMBER += 1
    EDIT_NUMBER = 0


def load_connection_map():
    """Loads the folder connection map from the Memory_connections_map.txt file."""
    connection_map = {}
    try:
        script_path = os.path.abspath(os.path.dirname(__file__))
        connection_map_path = os.path.join(script_path, "memory", "Memory_connections_map.txt")
        with open(connection_map_path, 'r') as file:
            for line in file:
                if line.strip():
                    parts = line.split("****")
                    if len(parts) >= 3:
                        folder_name = parts[0].strip()
                        folder_path = parts[2].strip().replace("Path: ", "")
                        # Normalize the folder path:
                        folder_path = folder_path.replace("//", "/").replace("\\", "/")
                        connection_map[folder_name] = folder_path
    except FileNotFoundError:
        print(f"{RED}Error: Connection map file not found.{RESET}")
    return connection_map


counter = 0
while True:
    user_input = process_user_input()
    timestamp = datetime.now().strftime(TIMESTAMP_FORMAT)
    response1 = call_interaction_model(user_input, timestamp)
    if response1:
        response2 = call_memory_model(user_input, response1.text)
        if response2:
            memory_entries = extract_entries_smart(response2.text)
            for entry in memory_entries:
                store_memory_frame(user_input, response1.text, response2.text, entry)  # Removed the 'check' comment