import os
import json
import re
from datetime import datetime
from fuzzywuzzy import fuzz
from collections import defaultdict

def  print_ascii_smile():
    print("print_ascii_smile")
FUNCTION_MAPPING = {
    "print_ascii_smile": print_ascii_smile,  # Add the function mapping here
}

def response_interpreter_for_function_calling(response):
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
    except Exception as E:
        print(E)
    if outcome is None:
        outcome = ""
    return outcome


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

def STORE_MEMORY_Frame(current_time, user_input, ai_response, ai_response2, memory_data):
    red = "\033[91m"
    green = "\033[92m"
    yellow = "\033[93m"
    blue = "\033[94m"
    magenta = "\033[95m"
    cyan = "\033[96m"
    white = "\033[97m"
    reset = "\033[0m"
    script_path = os.path.abspath(os.path.dirname(__file__))
    connection_map_path = os.path.join(script_path, "memories", "Memory_connecions_map.txt")
    with open(connection_map_path, 'r', encoding='utf-8') as f:
        connection_map_data = f.read()
    connection_map = defaultdict(list)
    for line in connection_map_data.splitlines():
        if "****" in line:
            current_folder_name = line.strip("****").strip()
        elif "  Path:" in line:
            path = line.strip("  Path:").strip()
            connection_map[current_folder_name].append(path)

    def extract_entries_smart(response_message):
        entries = []
        json_match = re.search(r"```json\n(.*?)\n```", response_message, re.DOTALL)
        if json_match:
            try:
                json_data = json_match.group(1)
                response_data = json.loads(json_data)
                entry = defaultdict(list)
                single_value_fields = {
                    "concise_summary",
                    "main_topic",
                    "problem_solved",
                    "concept_definition",
                    "category",
                    "subcategory",
                    "memory_about",
                    "interaction_type",
                    "positive_impact",
                    "negative_impact",
                    "expectations",
                    "object_states",
                    "short_description",
                    "description",
                    "strength_of_experience",
                    "personal_information",
                    "obtained_knowledge"
                }
                list_type_fields = {
                    "keywords",
                    "entities",
                    "actions",
                    "facts",
                    "contradictions_paradoxes",
                    "people",
                    "objects",
                    "animals",
                    "scientific_data",
                    "tags",
                    "tools_and_technologies",
                    "example_projects",
                    "best_practices",
                    "common_challenges",
                    "debugging_tips",
                    "related_concepts",
                    "visualizations",
                    "implementation_steps",
                    "resources",
                    "code_examples"
                }
                for key, value in response_data.items():
                    if key in single_value_fields:
                        if isinstance(value, list):
                            entry[key].extend(value)
                        else:
                            entry[key] = value
                    elif key in list_type_fields:
                        if isinstance(value, list):
                            if value and isinstance(value[0], dict):
                                entry[key].extend(value)
                            else:
                                entry[key].extend(value)
                        else:
                            entry[key].append(value)
                for key, value in response_data.items():
                    if "keyword" in key.lower() and isinstance(value, list):
                        entry["keywords"].extend(value)
                    elif "description" in key.lower():
                        entry["description"] = value
                    elif "summary" in key.lower():
                        entry["concise_summary"] = value
                    elif "step" in key.lower() and isinstance(value, list) and value and isinstance(value[0], dict):
                        entry["implementation_steps"].extend(value)
                    elif "resource" in key.lower() and isinstance(value, list) and value and isinstance(value[0], dict):
                        entry["resources"].extend(value)
                    elif "code" in key.lower() and isinstance(value, list) and value and isinstance(value[0], dict):
                        entry["code_examples"].extend(value)
                for key, value in response_data.items():
                    if "interaction_type" in key.lower() and isinstance(value, list):
                        entry["interaction_type"].extend(value)
                    elif "category" in key.lower():
                        entry["category"] = value
                    elif "subcategory" in key.lower():
                        entry["subcategory"] = value
                entry["storage"] = {
                    "storage_method": "",
                    "location": "",
                    "memory_folders_storage": [],
                    "strenght of matching memory to given folder": []
                }
                entries.append(dict(entry))
            except json.JSONDecodeError:
                print(f"{red}Error: Invalid JSON in response message.{reset}")
            except Exception as e:
                print(f"{red}Error extracting entry: {e}{reset}")
        return entries

    extracted_entries = extract_entries_smart(ai_response2)

    if extracted_entries:
        for entry in extracted_entries:
            matching_folders = []
            category, time_period, keyword = categorize_memory(entry["concise_summary"], connection_map)
            if category and time_period:
                matching_folders = connection_map.get(f"{category} - {time_period}", [])
            if matching_folders:
                matching_scores = []
                for folder in matching_folders:
                    parts = folder.split("\\")[-2:]
                    category = parts[0]
                    time_period = parts[1]
                    similarity_score = fuzz.ratio(entry["concise_summary"], f"{category} {time_period}")
                    matching_scores.append((folder, similarity_score))
                entry["storage"]["memory_folders_storage"] = matching_folders
                entry["storage"]["strenght of matching memory to given folder"] = matching_scores
                script_path = os.path.abspath(os.path.dirname(__file__))
                memory_frame_number = memory_data.get('MEMORY_FRAME_NUMBER', 1)
                edit_number = memory_data.get('EDIT_NUMBER', 0)
                timestamp_format = "%Y-%m-%d_%H-%M-%S"
                timestamp = current_time.strftime(timestamp_format)
                for folder, similarity_score in matching_scores:
                    file_name_suffix = ""
                    if similarity_score != "unknown":
                        file_name_suffix = f"_strenght_{similarity_score}"
                    memory_frame_filepath = os.path.join(script_path, folder,
                                                         f"MemoryFrame_{memory_frame_number}_{edit_number}_{timestamp}{file_name_suffix}.json")
                    os.makedirs(os.path.join(script_path, folder), exist_ok=True)
                    with open(memory_frame_filepath, "w") as f:
                        json.dump(entry, f, indent=4)
                    os.makedirs(os.path.join(script_path, "memory_logs"), exist_ok=True)
                    memory_log_filepath = os.path.join(script_path, "memory_logs", "MemoryFrames_log.txt")
                    with open(memory_log_filepath, 'a', encoding='utf-8') as f:
                        f.write(
                            f"MemoryFrame: {memory_frame_number}, Edit: {edit_number}, Type: JSON, path: {memory_frame_filepath}, time: {timestamp}, session: {memory_frame_number}_{edit_number}\n"
                        )
    else:
        print(f"{yellow}No JSON data found in the AI response{reset}")
    separator = "######$######"
    conversation_filename = f"MemoryFrame_{timestamp}.txt"
    conversation_filepath = os.path.join(script_path, "conversation_logs", conversation_filename)
    readable_timestamp = current_time.strftime('%Y-%m-%d %H:%M:%S')
    frame_content = (
        f"{separator} Memory Frame {memory_frame_number}, Edit {edit_number} - {readable_timestamp} {separator}\n"
        f"USER_INPUT: {user_input}\n"
        f"AI_RESPONSE: {ai_response}\n"
        f"AI_RESPONSE_SUMMARY: {ai_response2}\n"
        f"{separator} Memory Frame End {memory_frame_number}, Edit {edit_number} {separator}\n\n"
    )
    with open(conversation_filepath, 'a', encoding='utf-8') as f:
        f.write(frame_content)
    memory_data['MEMORY_FRAME_NUMBER'] += 1
    os.makedirs(os.path.join(script_path, "memory_logs"), exist_ok=True)
    memory_log_filepath = os.path.join(script_path, "memory_logs", "MemoryFrames_log.txt")
    with open(memory_log_filepath, 'a', encoding='utf-8') as f:
        f.write(
            f"MemoryFrame: {memory_frame_number - 1}, Edit: {edit_number}, Type: Text, path: {conversation_filepath}, time: {timestamp}, session: {memory_frame_number - 1}_{edit_number}\n"
        )

def categorize_memory(summary, connection_map):
    """Categorizes a memory based on its summary."""
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
    import google.generativeai as genai
    genai.configure(api_key='YOUR_API_KEY')  # Replace with your API key

    memory_data = {
        'MEMORY_FRAME_NUMBER': 1,
        'EDIT_NUMBER': 0
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
            formatted_timestamp = current_time.strftime('%Y-%m-%d_%H-%M-%S')
            chat1 = interaction_model.start_chat(history=[])
            prompt = f"currentTime:  {formatted_timestamp}  create {user_input} "
            response1 = chat1.send_message(prompt)
            try:
                print_colored(f"AI Response: {response1.text}", "green")
            except Exception as e:
                print(e)


            """
             memory_model = genai.GenerativeModel(
                model_name='gemini-1.5-flash-latest',
                safety_settings={'HARASSMENT': 'block_none'},
                system_instruction
                tools=[]    <--  for  futre  integration passing  funcion  descriptions in specifid  Gemini   format  like 
                {
    'function_declarations': [
        {
            'name': 'save_to_file',
            'description': 'Saves content to a file.',
            'parameters': {
                'type_': 'OBJECT',
                'properties': {
                    'content': {'type_': 'STRING'},
                    'file_name': {'type_': 'STRING', 'description': 'The name of the file. Defaults to "NoName".'},
                    'file_path': {'type_': 'STRING', 'description': 'The path to save the file. Defaults to the current working directory if not provided.'}
                },
                'required': ['content', 'file_name']
            }
        }
    ]
}
                
                
                
            
            """
            memory_model = genai.GenerativeModel(
                model_name='gemini-1.5-flash-latest',
                safety_settings={'HARASSMENT': 'block_none'},
                system_instruction="""You are a sophisticated AI assistant helping to organize memories. 
                    Analyze and summarize the above user-AI conversation, focusing on elements that would be most useful for storing and retrieving this memory later. Don't hallucinate.
                    use provided schema  for  response
                    Provide the following information in a structured format using JSON:  you  have  2 Templates to choose form

                    you can also  cut  out entries  if  they  dont  seem  approparate for  memory storage and would be  empty
                    never  crose  out   "Memory Folder storage entry": 
                    """,
            )
            schema_for_chat2 = """   
                                if  the memory  does  not  fit  into schema  you can  reduce  entries  and  focues  on most  important entries:
                                but  always  use  "memory_folders_storage": as  suggestion  in what  folders  that   memor should be saved.

                                Template  to use:          
                                         {
                              "metadata": {
                                "creation_date": "", // Date and time the memory was created.
                                "source": "", // Origin of the memory (e.g., conversation, website, book).
                                "author": "" // Author or source of the memory.
                              },
                              "type": "conversation" // OR "technical_concept"  (This field designates the memory type)
                              "core": {
                                "main_topic": "",  // Core theme or subject of the memory.
                                "category": "",  // General category (e.g., "Technology", "History", "Science").
                                "subcategory": "", // More specific category (e.g., "Programming", "World War II", "Biology").
                                "memory_about": "" // Brief description of what the memory is about.
                              },
                              "summary": {
                                "concise_summary": "", // Brief overview of the memory's content.
                                "description": "" //  Detailed explanation of the memory.
                              },
                              "content": {
                                "keywords": [], // Key terms related to the memory.
                                "entities": [], // People, places, things mentioned.
                                "tags": [], // User-defined tags for retrieval.
                                "observations": [], //  Interesting observations or insights made.
                                "facts": [], //  Statements of fact in the memory.
                                "contradictions": [], //  Contradictions or conflicting statements. 
                                "paradoxes": [], //  Paradoxes or seemingly contradictory ideas. 
                                "scientific_data": [], //  Scientific data or observations.
                                "visualizations": [], //  Visualizations or diagrams related to the memory.
                              },
                              "interaction": {
                                "interaction_type": [], // Type of interaction that occurred (e.g., "Question-Answer", "Discussion", "Instruction-Following"). 
                                "people": [], //  People involved in the memory.
                                "objects": [], //  Objects involved in the memory.
                                "animals": [], //  Animals involved in the memory. 
                                "actions": [], // Actions or events described in the memory. 
                                "observed_interactions": [], //  Additional interactions observed.
                              },
                              "impact": {
                                "obtained_knowledge": "", //  New knowledge or insights gained.
                                "positive_impact": "", // Positive outcomes of the memory.
                                "negative_impact": "", //  Negative outcomes of the memory.
                                "expectations": "", //  User expectations before the interaction.
                                "strength_of_experience": "" // Significance of the memory for the user.
                              },
                              "importance": {
                                "reason": "", //  Why this memory is significant or important. 
                                "potential_uses": [] //  How this memory might be used or applied in the future.
                              },
                              "technical_details": { 
                                 "problem_solved": "", // (For technical concepts)  The problem being addressed.
                                 "concept_definition": "", // (For technical concepts) A clear definition of the term. 
                                 "implementation_steps": [
                                   {
                                     "step": "",
                                     "code_snippet": "",
                                     "notes": ""
                                   }
                                 ], //  Implementation steps for a technical concept. 
                                 "tools_and_technologies": [], //  Tools or technologies used for implementation.
                                 "example_projects": [], //  Examples of real-world projects using the concept.
                                 "best_practices": [], //  Best practices for implementation.
                                 "common_challenges": [], //  Common difficulties encountered.
                                 "debugging_tips": [], //  Tips for troubleshooting.
                                 "related_concepts": [], //  Other related concepts. 
                                 "resources": [
                                   {
                                     "type": "",
                                     "url": "",
                                     "title": ""
                                   }
                                 ], // Relevant resources (articles, books, videos).
                                 "code_examples": [
                                   {
                                     "name": "",
                                     "description": "",
                                     "code": "",
                                     "notes": ""
                                   }
                                 ], // Code examples relevant to the memory. 
                              },
                              "storage": {
                                "storage_method": "", //  How the memory is stored (e.g., database, file system).
                                "location": "", //  The location where the memory is stored.
                                "memory_folders_storage": [] //  Suggested folders for storage.
                                "strenght of matching memory to given folder": [] //  from scale 0-10
                              }
                            }

            """
            chat_2 = memory_model.start_chat(history=[])
            create_memory_prompt = f"""User: {user_input}
                                    AI: {response1.text}
                                    Schema:
                                    {schema_for_chat2}"""
            response2 = chat_2.send_message(create_memory_prompt)
            response_interpreter_for_function_calling(response2)
            try:
                STORE_MEMORY_Frame(
                    current_time,
                    user_input,
                    response1.text,
                    response2.text,
                    memory_data
                )
            except Exception as e:
                print(e)
        except Exception as e:
            print_colored(f"Error in the main loop: {e}", "red")