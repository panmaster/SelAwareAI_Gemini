import os
import json
import re
from datetime import datetime
from collections import defaultdict
import google.generativeai as genai
from termcolor import colored, cprint  # Import termcolor for colored printing

# Configure the Google Generative AI API
genai.configure(api_key='AIzaSyCOaR8htDQH_kbQatacCksT60S26I_F-QU')  # Replace with your API key


# Function to print an ASCII smile (for demonstration)
def print_ascii_smile():
    print("print_ascii_smile")


# Mapping of function names to functions for dynamic function calling
FUNCTION_MAPPING = {
    "print_ascii_smile": print_ascii_smile
}


# Function to print colored text for improved readability
def print_colored(text, color):
    """Prints text with the specified color."""
    colors = {
        "red": "\033[91m",
        "green": "\033[92m",
        "yellow": "\033[93m",
        "blue": "\033[94m",
        "magenta": "\033[95m",
        "cyan": "\033[96m",
        "white": "\033[97m",
        "reset": "\033[0m"
    }
    print(f"{colors.get(color, '')}{text}{colors['reset']}")


# Function to interpret AI responses and execute function calls
def response_interpreter_for_function_calling(response):
    """Interprets the AI response and executes function calls if present."""
    outcome = ""
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
                                cprint(f"Function Call Exit: {function_name}", 'cyan')
                            except Exception as e:
                                cprint(f"Error executing function {function_name}: {e}", "red")
                        else:
                            cprint("Warning: Function call arguments are missing.", "red")
                    else:
                        cprint(f"Error: Unknown function: {function_name}", "red")
                else:
                    cprint("No function call found in the response.", "blue")
    except Exception as e:
        cprint(f"Error in response interpreter: {e}", "red")
    return outcome


# Function to store memory frames based on AI responses
def store_memory_frame(current_time, user_input, ai_response, ai_summary, memory_data):
    """Stores a memory frame based on AI response and folder structure."""

    # Get the current script's directory
    script_path = os.path.abspath(os.path.dirname(__file__))

    # Construct the relative path to the connection map file
    connection_map_path = os.path.join(script_path, "memories", "Memory_connections_map.txt")

    # Load the connection map (folder structure)
    connection_map = defaultdict(list)
    try:
        with open(connection_map_path, 'r', encoding='utf-8') as f:
            cprint(f"Reading Connection Map: {connection_map_path}", 'green')
            for line in f:
                if "****" in line:
                    current_folder_name = line.strip("****").strip()
                elif "Path:" in line:
                    path = line.strip("Path:").strip()
                    connection_map[current_folder_name].append(path)
    except FileNotFoundError:
        cprint(f"File not found. Creating: {connection_map_path}", 'yellow')
        # Create an empty file
        with open(connection_map_path, 'w', encoding='utf-8') as f:
            f.write("")
    except Exception as e:
        cprint(f"Error reading file: {e}", "red")

    # Extract structured data from the AI summary
    extracted_entries = extract_entries_smart(ai_summary)

    cprint("Extracted Entries:", 'blue')
    cprint(f"{extracted_entries}", 'blue')

    if extracted_entries:
        for entry in extracted_entries:
            suggested_folders = entry["storage"].get("memory_folders_storage", [])
            cprint(f"Suggested Folders:", 'magenta')
            cprint(f"{suggested_folders}", 'magenta')

            # Sort folders by probability, limiting to the top 6
            suggested_folders.sort(key=lambda x: x.get("probability", 0), reverse=True)
            suggested_folders = suggested_folders[:6]
            cprint(f"Sorted Folders:", 'cyan')
            cprint(f"{suggested_folders}", 'cyan')

            for folder_info in suggested_folders:
                folder_path = folder_info.get("folder_path")
                probability = folder_info.get("probability", 0)  # Default probability to 0 if not provided
                strength_of_matching_memory_to_given_folder = folder_info.get(
                    'strength_of_matching_memory_to_given_folder', 0)

                # Check if the folder exists in the connection map
                matching_folders = connection_map.get(folder_path, [])
                cprint(f"Matching Folders for {folder_path}:", 'yellow')
                cprint(f"{matching_folders}", 'yellow')

                if matching_folders:
                    # Construct the file path for the memory frame
                    memory_frame_number = memory_data.get('MEMORY_FRAME_NUMBER', 1)
                    edit_number = memory_data.get('EDIT_NUMBER', 0)
                    timestamp = current_time.strftime("%Y-%m-%d_%H-%M-%S")
                    ai_suggested_name = entry.get("naming_suggestion", {}).get("memory_frame_name", "")
                    file_name = f"MemoryFrame_{memory_frame_number}_{edit_number}_{timestamp}_{ai_suggested_name}_strength_{probability}_{strength_of_matching_memory_to_given_folder}.json"
                    memory_frame_filepath = os.path.join(script_path, folder_path, file_name)

                    cprint(f"Memory Frame Filepath: {memory_frame_filepath}", 'green')

                    # Create the folder if it doesn't exist
                    os.makedirs(os.path.join(script_path, folder_path), exist_ok=True)

                    try:
                        # Save the memory frame data to a JSON file
                        with open(memory_frame_filepath, "w") as f:
                            cprint(f"Saving Memory Frame to: {memory_frame_filepath}", 'green')
                            json.dump(entry, f, indent=4)

                        # Update the memory log file
                        os.makedirs(os.path.join(script_path, "memory_logs"), exist_ok=True)
                        memory_log_filepath = os.path.join(script_path, "memory_logs", "MemoryFrames_log.txt")
                        with open(memory_log_filepath, 'a', encoding='utf-8') as f:
                            f.write(
                                f"MemoryFrame: {memory_frame_number}, Edit: {edit_number}, Type: JSON, path: {memory_frame_filepath}, time: {timestamp}, session: {memory_frame_number}_{edit_number}\n"
                            )
                        cprint(f"Memory Log Updated: {memory_log_filepath}", 'green')
                    except Exception as e:
                        cprint(f"Error saving memory frame: {e}", "red")

    # Save the conversation log (user input and AI responses)
    separator = "######$######"
    conversation_filename = f"MemoryFrame_{timestamp}.txt"
    conversation_filepath = os.path.join(script_path, "conversation_logs", conversation_filename)
    readable_timestamp = current_time.strftime('%Y-%m-%d %H:%M:%S')
    frame_content = (
        f"{separator} Memory Frame {memory_frame_number}, Edit {edit_number} - {readable_timestamp} {separator}\n"
        f"USER_INPUT: {user_input}\n"
        f"AI_RESPONSE: {ai_response}\n"
        f"AI_SUMMARY: {ai_summary}\n"
        f"{separator} Memory Frame End {memory_frame_number}, Edit {edit_number} {separator}\n\n"
    )

    with open(conversation_filepath, 'a', encoding='utf-8') as f:
        f.write(frame_content)
    cprint(f"Conversation Log Saved: {conversation_filepath}", 'green')

    # Increment the memory frame number for the next interaction
    memory_data['MEMORY_FRAME_NUMBER'] += 1
    os.makedirs(os.path.join(script_path, "memory_logs"), exist_ok=True)
    memory_log_filepath = os.path.join(script_path, "memory_logs", "MemoryFrames_log.txt")
    with open(memory_log_filepath, 'a', encoding='utf-8') as f:
        f.write(
            f"MemoryFrame: {memory_frame_number - 1}, Edit: {edit_number}, Type: Text, path: {conversation_filepath}, time: {timestamp}, session: {memory_frame_number - 1}_{edit_number}\n"
        )
    cprint(f"Memory Log Updated: {memory_log_filepath}", 'green')


# Function to extract structured entries from AI responses using regular expressions
def extract_entries_smart(response_message):
    """Extracts structured JSON data from the AI response."""
    entries = []
    json_match = re.search(r"```json\n(.*?)\n```", response_message, re.DOTALL)
    if json_match:
        try:
            json_data = json_match.group(1)
            response_data = json.loads(json_data)
            entry = defaultdict(list)

            # Define fields that should store a single value
            single_value_fields = {
                "concise_summary", "main_topic", "problem_solved", "concept_definition", "category",
                "subcategory", "memory_about", "interaction_type", "positive_impact",
                "negative_impact", "expectations", "object_states", "short_description",
                "description", "strength_of_experience", "personal_information", "obtained_knowledge"
            }

            # Define fields that should store a list of values
            list_type_fields = {
                "keywords", "entities", "actions", "facts", "contradictions_paradoxes",
                "people", "objects", "animals", "scientific_data", "tags",
                "tools_and_technologies", "example_projects", "best_practices", "common_challenges",
                "debugging_tips", "related_concepts", "visualizations", "implementation_steps",
                "resources", "code_examples"
            }

            for key, value in response_data.items():
                if key in single_value_fields:
                    entry[key] = value if not isinstance(value, list) else (value[0] if value else "")
                elif key in list_type_fields:
                    entry[key].extend(value if isinstance(value, list) else [value])

            # Handle the 'storage' field specifically
            entry["storage"] = {
                "storage_method": "",
                "location": "",
                "memory_folders_storage": response_data.get("storage", {}).get("memory_folders_storage", []),
                "strength_of_matching_memory_to_given_folder": []
            }

            # Validate "probability" values in 'memory_folders_storage'
            for folder_info in entry["storage"]["memory_folders_storage"]:
                probability = folder_info.get("probability")
                if probability is not None and not 0 <= probability <= 10:
                    print(
                        f"Warning: Invalid probability value '{probability}' found in memory_folders_storage. Valid range is 0 to 10."
                    )

            entries.append(dict(entry))
        except json.JSONDecodeError:
            cprint("Error: Invalid JSON in the AI response.", "red")
        except Exception as e:
            cprint(f"Error extracting entry: {e}", "red")
    return entries


# Function to categorize a memory based on its summary (not used in the current code)
def categorize_memory(summary, connection_map):
    """Categorizes a memory based on its summary (not currently used)."""
    category = ""
    time_period = ""
    keyword = ""
    for folder_name, paths in connection_map.items():
        parts = folder_name.split(" - ")
        if parts:
            potential_category = parts[0]
            potential_time_period = parts[1] if len(parts) > 1 else None
            if potential_category.lower() in summary.lower():
                category = potential_category
                time_period = potential_time_period
                keyword = potential_category
                break
    return category, time_period, keyword


# --- Main Loop (Memory Frame Creation) ---
if __name__ == "__main__":
    memory_data = {'MEMORY_FRAME_NUMBER': 1, 'EDIT_NUMBER': 0}

    while True:
        try:
            user_input = input("Enter input: ")
            current_time = datetime.now()
            timestamp = current_time.strftime('%Y-%m-%d_%H-%M-%S')

            cprint(f"User Input: {user_input}", 'cyan')
            cprint(f"Current Time: {current_time}", 'cyan')
            cprint(f"Timestamp: {timestamp}", 'cyan')

            # --- Interaction Model ---
            interaction_model = genai.GenerativeModel(
                model_name='gemini-1.5-flash-latest',
                safety_settings={'HARASSMENT': 'block_none'},
                system_instruction='You follow orders and generate creative text interactions'
            )
            chat1 = interaction_model.start_chat(history=[])
            response1 = chat1.send_message(f"currentTime: {timestamp} create {user_input}")
            cprint(f"AI Response: {response1.text}", 'green')

            # --- Memory Model ---
            memory_model = genai.GenerativeModel(
                model_name='gemini-1.5-flash-latest',
                safety_settings={'HARASSMENT': 'block_none'},
                system_instruction="""You are a sophisticated AI assistant helping to organize memories. 
                    Analyze and summarize the above user-AI conversation, focusing on elements that would be most useful for storing and retrieving this memory later. Don't hallucinate. 
                    Use the provided JSON schema for your response and fill in all fields with relevant information.
                    You can omit entries if they don't seem appropriate for memory storage and would be empty.
                    Never omit the "memory_folders_storage" entry.

                    **JSON Schema:**

                    ```json
                    {
                      "metadata": {
                        "creation_date": "", // Date and time when the memory frame was created
                        "source": "", // Source of the information (e.g., conversation, external resource)
                        "author": "" // Author or source of the information (e.g., user, AI)
                      },
                      "type": "conversation", // OR "technical_concept" - Type of memory (e.g., conversation, technical concept, personal experience)
                      "core": {
                        "main_topic": "", // Primary subject or theme of the memory
                        "category": "", // Broad category for the memory (e.g., Deep Learning, History, Personal Life)
                        "subcategory": "", // More specific subcategory for the memory (e.g., Convolutional Neural Networks, 20th Century, Relationships)
                        "memory_about": "" // A brief description of what the memory is about
                      },
                      "summary": {
                        "concise_summary": "", // Short and to-the-point summary of the memory content
                        "description": "" // More detailed description of the memory content
                      },
                      "content": {
                        "keywords": [], // List of important keywords related to the memory
                        "entities": [], // List of entities mentioned in the memory (e.g., people, places, organizations)
                        "tags": [], // List of additional tags for organization and retrieval (e.g., "strength_10", "holiday_in_Greece", "AI_ethics")
                        "observations": [], // List of key observations or insights from the memory
                        "facts": [], // List of factual statements or data from the memory
                        "contradictions": [], // List of identified contradictions or conflicting information
                        "paradoxes": [], // List of identified paradoxes or contradictions
                        "scientific_data": [], // List of scientific data or findings from the memory
                        "visualizations": [] // List of visualizations or diagrams related to the memory
                      },
                      "interaction": {
                        "interaction_type": [], // Type of interaction (e.g., conversation, observation, experiment)
                        "people": [], // List of people involved in the memory
                        "objects": [], // List of objects involved in the memory
                        "animals": [], // List of animals involved in the memory
                        "actions": [], // List of actions taken in the memory
                        "observed_interactions": [] // List of observed interactions (e.g., conversations between others)
                      },
                      "impact": {
                        "obtained_knowledge": "", // What new knowledge was gained from the memory
                        "positive_impact": "", // Positive impact or benefits of the memory
                        "negative_impact": "", // Negative impact or drawbacks of the memory
                        "expectations": "", // Expectations or goals related to the memory
                        "strength_of_experience": "" // Subjective strength or intensity of the memory
                      },
                      "importance": {
                        "reason": "", // Reasons why the memory is important or significant
                        "potential_uses": [] // Potential uses or applications of the memory
                      },
                      "technical_details": {
                        "problem_solved": "", // The problem that was solved in the memory
                        "concept_definition": "", // Definition of a concept or term from the memory
                        "implementation_steps": [], // Steps taken to implement something in the memory
                        "tools_and_technologies": [], // Tools or technologies used in the memory
                        "example_projects": [], // Example projects related to the memory
                        "best_practices": [], // Best practices identified in the memory
                        "common_challenges": [], // Common challenges encountered in the memory
                        "debugging_tips": [], // Debugging tips or strategies from the memory
                        "related_concepts": [], // Related concepts or topics discussed in the memory
                        "resources": [], // Resources (e.g., articles, websites, books) mentioned in the memory
                        "code_examples": [] // Code examples from the memory
                      },
                      "storage": {
                        "storage_method": "", // How the information should be stored (e.g., text, JSON, image)
                        "location": "", // Location where the information should be stored (e.g., folder path)
                        "memory_folders_storage": [
                          {
                            "folder_path": "", // Suggested folder path for storing the memory
                            "probability": 0 // Probability score (0-10) indicating the likelihood of the memory belonging to the folder
                          }
                        ],
                        "strength_of_matching_memory_to_given_folder": [] // List of strength scores for each folder
                      },
                      "naming_suggestion": {
                        "memory_frame_name": "", // Proposed name for the memory frame
                        "explanation": "" // Optional: Explanation of the reasoning behind the chosen name
                      }
                    }
                    ```

                    **Memory Storage Suggestions:**
                    Provide your suggestions for where this memory frame should be stored using the following format within the "memory_folders_storage" field:

                    * **"folder_path":** The relative path for storing the memory frame (use '/' as the path separator).
                    * **"probability":** The strength of probability (from 0 to 10) that the memory frame should be stored in the suggested folder. Use a scale from 0 (least likely) to 10 (most likely) to express your confidence. 
                """
            )
            chat2 = memory_model.start_chat(history=[])
            create_memory_prompt = f"User: {user_input}\nAI: {response1.text}"
            response2 = chat2.send_message(create_memory_prompt)
            cprint(f"Memory Model Response: {response2.text}", 'green')

            # Interpret the response for function calls
            response_interpreter_for_function_calling(response2)

            # Store the memory frame based on the AI's analysis
            store_memory_frame(current_time, user_input, response1.text, response2.text, memory_data)

        except Exception as e:
            cprint(f"Error in the main loop: {e}", "red")