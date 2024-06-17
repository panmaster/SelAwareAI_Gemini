
import google.generativeai as genai



genai.configure(api_key='AIzaSyDRJJmMsB7WQXQ8P0mKTCHf9VIx5uprTw8')  # Replace with your actual API key
import os
import re
import json
import pathlib
from datetime import datetime
from collections import defaultdict


BLACK = "\033[30m"
RED = "\033[31m"
GREEN = "\033[32m"
YELLOW = "\033[33m"
BLUE = "\033[34m"
MAGENTA = "\033[35m"
CYAN = "\033[36m"
WHITE = "\033[37m"
RESET = "\033[0m"
BOLD = "\033[1m"
UNDERLINE = "\033[4m"
REVERSE = "\033[7m"

MEMORY_FRAME_NUMBER = 1
EDIT_NUMBER = 0
TIMESTAMP_FORMAT = '%Y-%m-%d_%H-%M'

def sanitize_href(href, memories_folder_path):
    """Sanitizes a given href string by replacing spaces with %20."""
    href = href.replace(" ", "%20")
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
            relative_path = os.path.relpath(memory_frame_path, memories_folder_path)
            href = sanitize_href(relative_path, memories_folder_path)
            html_insertion += f"""
                       <li><a href='{href}'>{os.path.basename(href)}</a></li> 
                   """

        html_insertion += "</ul>"

        with open(log_file_path, 'a') as log_file:
            log_file.write(html_insertion)

        print(f"{GREEN}HTML logs updated successfully.{RESET}")
    except Exception as e:
        print(f"Error updating HTML logs: {e}")

def Get_path_of_memories_folder():
    """Returns the absolute path to the 'memories' folder."""
    current = pathlib.Path.cwd()
    memories_path = current / "memories"
    return memories_path.absolute()

def process_user_input():
    user_input = input(f"{GREEN}Enter input: {RESET}")
    print(f"{MAGENTA}User input received: {user_input}{RESET}")
    return user_input

def call_interaction_model(user_input, timestamp):
    print(f"\n{CYAN}--- Calling Interaction Model ---{RESET}")
    try:
        interaction_model = genai.GenerativeModel(
            model_name='gemini-1.5-flash-latest',
            safety_settings={'HARASSMENT': 'block_none'},
            system_instruction='You follow orders and generate creative text interactions'
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
            system_instruction="""You are a sophisticated AI assistant helping to organize memories. 
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
              "core": {
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
            Here  you have  existing  folder structure  for  memory_folders_storage [{
    "Actions & Results": {
        "Actions & Results": {
            "Future": {},
            "Past": {},
            "Present": {}
        }
    },
    "BaseFileStructure.txt": [],
    "Challenges & Setbacks": {
        "Areas for Improvement": {},
        "Difficult Emotions": {
            "Anger & Frustration": {},
            "Fear & Anxiety": {},
            "Jealousy & Envy": {},
            "Sadness & Grief": {},
            "Shame & Guilt": {},
            "Trauma & Abuse": {
                "Experiences": {},
                "Healing Journey": {},
                "Impact": {}
            }
        },
        "Failures & Disappointments": {
            "In Career": {},
            "In Personal Projects": {},
            "In Relationships": {}
        },
        "Negative Thought Patterns": {},
        "Significant Mistakes": {
            "Description": {},
            "How I Grew": {},
            "Lessons Learned": {}
        }
    },
    "CoreMemory": {
        "Conceptual Exploration": {
            "Contradictions & Dilemmas": {},
            "Paradoxes & Contradictions": {},
            "Unknowns & Mysteries": {}
        },
        "Core Experiences": {
            "Challenges Faced": {
                "External Challenges": {
                    "Obstacles": {
                        "How I Overcame Them": {},
                        "Types of Obstacles": {},
                        "What I Learned": {}
                    },
                    "Setbacks": {
                        "How I Recovered": {},
                        "Types of Setbacks": {},
                        "What I Learned": {}
                    }
                },
                "Internal Challenges": {
                    "Fear & Anxiety": {
                        "How I Coped": {},
                        "Specific Fears": {},
                        "What I Learned": {}
                    },
                    "Negative Thought Patterns": {
                        "Common Negative Thoughts": {},
                        "Strategies for Changing Them": {},
                        "What I Learned": {}
                    },
                    "Self-Doubt": {
                        "How I Overcame It": {},
                        "Sources of Self-Doubt": {},
                        "What I Learned": {}
                    }
                }
            },
            "Life-Changing Events": {
                "Negative": {},
                "Positive": {}
            },
            "Significant Moments": {
                "Other": {},
                "Personal": {},
                "Professional": {},
                "Travel": {}
            },
            "Triumphs & Accomplishments": {
                "Creative Wins": {
                    "Creative Works": {},
                    "Impact on Life": {},
                    "Recognition & Awards": {}
                },
                "Personal Achievements": {
                    "Goals Achieved": {},
                    "Impact on Life": {},
                    "Personal Growth": {}
                },
                "Professional Successes": {
                    "Career Growth": {},
                    "Impact on Life": {},
                    "Projects & Achievements": {}
                }
            },
            "Turning Points": {
                "In Career": {},
                "In Personal Growth": {},
                "In Relationships": {},
                "Other": {}
            }
        },
        "Goals & Visions": {
            "Life Vision": {
                "Long-Term Goals": {},
                "Mid-Term Goals": {},
                "Short-Term Goals": {}
            },
            "Personal Goals": {
                "Long-Term Goals": {},
                "Mid-Term Goals": {},
                "Short-Term Goals": {}
            }
        },
        "Knowledge Base": {
            "Areas of Expertise": {},
            "Key Concepts & Theories": {},
            "Personal Beliefs & Values": {}
        },
        "Reflections & Insights": {
            "Lessons Learned": {
                "From Mistakes": {},
                "From Relationships": {},
                "From Successes": {}
            },
            "Self-Discovery": {
                "Areas for Growth": {},
                "Strengths & Talents": {},
                "What I've Learned About Myself": {}
            }
        },
        "Relationships": {
            "Family": {
                "Extended Family": {
                    "Challenges Faced": {},
                    "Impact on My Life": {},
                    "Lessons Learned": {},
                    "Memorable Moments": {}
                },
                "Parents": {
                    "Challenges Faced": {},
                    "Impact on My Life": {},
                    "Lessons Learned": {},
                    "Memorable Moments": {}
                },
                "Siblings": {
                    "Challenges Faced": {},
                    "Impact on My Life": {},
                    "Lessons Learned": {},
                    "Memorable Moments": {}
                }
            },
            "Friendships": {
                "Circles & Groups": {
                    "Impact on My Life": {},
                    "Lessons Learned": {},
                    "Shared Experiences": {}
                },
                "Close Friends": {
                    "Challenges Faced": {},
                    "Impact on My Life": {},
                    "Lessons Learned": {},
                    "Memorable Moments": {}
                },
                "Meaningful Interactions": {
                    "Impact on My Life": {},
                    "Lessons Learned": {},
                    "Unexpected Encounters": {}
                }
            },
            "Romantic Relationships": {
                "Partners": {
                    "Challenges Faced": {},
                    "Impact on My Life": {},
                    "Lessons Learned": {},
                    "Memorable Moments": {}
                },
                "Relationship Milestones": {
                    "First Date": {},
                    "First Kiss": {},
                    "Marriage": {},
                    "Moving In Together": {},
                    "Other Milestones": {}
                }
            }
        }
    },
    "Emotional Landscape": {
        "Dominant Emotions": {},
        "Emotional Triggers": {}
    },
    "Emotions & Reflections": {
        "Emotional Experiences": {
            "Dominant Emotions": {},
            "Emotional Triggers": {}
        },
        "Personal Growth & Insights": {
            "Lessons Learned": {},
            "Self-Discovery": {}
        }
    },
    "Goals & Aspirations": {
        "Life Vision": {
            "Aspirations": {},
            "Dreams": {},
            "Values & Beliefs": {}
        },
        "Personal Goals": {
            "Creative Pursuits": {},
            "Health & Wellbeing": {},
            "Other Personal Goals": {},
            "Personal Development": {},
            "Relationships": {}
        },
        "Professional Goals": {
            "Career Advancement": {},
            "Other Professional Goals": {},
            "Project Goals": {},
            "Skills & Expertise": {}
        }
    },
    "Knowledge & Learning": {
        "Formal Education": {
            "Degrees & Certifications": {},
            "Schools": {},
            "Significant Projects": {}
        },
        "Knowledge Base": {
            "Artistic Movements": {},
            "Cultural Insights": {},
            "Facts & Concepts": {},
            "Historical Events": {},
            "Philosophical Ideas": {},
            "Scientific Discoveries": {}
        },
        "Laws & Regulations": {
            "Legal Knowledge": {},
            "Personal Experiences with Laws": {},
            "Understanding of Legal Systems": {}
        },
        "Self-Directed Learning": {
            "Areas of Interest": {},
            "Learning Resources": {
                "Bookshelf": {},
                "Mentors & Teachers": {},
                "Online Courses": {}
            },
            "Skills Acquired": {}
        }
    },
    "Life Events & Transitions": {
        "Life Transitions": {
            "Health & Wellbeing": {
                "Habits & Routines": {},
                "Mental & Emotional Health": {},
                "Physical Health": {}
            },
            "Knowledge & Skills": {
                "Formal Education": {},
                "Self-Directed Learning": {},
                "Skills & Expertise": {}
            },
            "Personal Growth": {
                "Challenges Overcome": {},
                "Milestones": {},
                "Significant Decisions": {}
            },
            "Relationships": {
                "Family Dynamics": {},
                "Friendships": {},
                "Professional Connections": {},
                "Romantic Relationships": {}
            }
        },
        "Significant Events": {
            "Other": {},
            "Personal": {
                "Birthdays": {},
                "Graduations": {},
                "Other Personal Events": {},
                "Weddings": {}
            },
            "Professional": {
                "Job Changes": {},
                "Other Professional Events": {},
                "Project Completions": {},
                "Promotions": {}
            },
            "Travel": {
                "Moving Homes": {},
                "Other Travel Events": {},
                "Trips & Journeys": {}
            }
        }
    },
    "Planning & Progress": {
        "Plans & Strategies": {
            "Long-Term Plans": {},
            "Short-Term Plans": {},
            "Strategies Used": {
                "Goal Setting": {},
                "Other Strategies": {},
                "Problem Solving": {},
                "Time Management": {}
            }
        },
        "Progress & Outcomes": {
            "Goals Achieved": {},
            "Goals Not Achieved": {},
            "Lessons Learned from Progress": {},
            "Results of Actions": {
                "Negative Results": {},
                "Positive Results": {}
            }
        }
    }
}]
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
            single_value_fields = {
                "metadata.creation_date": "metadata",
                "metadata.source": "metadata",
                "metadata.author": "metadata",
                "type": "core",
                "core.main_topic": "core",
                "core.category": "core",
                "core.subcategory": "core",
                "core.memory_about": "core",
                "summary.concise_summary": "summary",
                "summary.description": "summary",
                "impact.obtained_knowledge": "impact",
                "impact.positive_impact": "impact",
                "impact.negative_impact": "impact",
                "impact.expectations": "impact",
                "impact.strength_of_experience": "impact",
                "importance.reason": "importance",
                "importance.importance_level": "importance",
                "technical_details.problem_solved": "technical_details",
                "naming_suggestion.memory_frame_name": "naming_suggestion",
                "naming_suggestion.explanation": "naming_suggestion"
            }
            list_type_fields = {
                "content.keywords": "content",
                "content.entities": "content",
                "content.tags": "content",
                "content.observations": "content",
                "content.facts": "content",
                "content.contradictions": "content",
                "content.paradoxes": "content",
                "content.scientific_data": "content",
                "content.visualizations": "content",
                "interaction.interaction_type": "interaction",
                "interaction.people": "interaction",
                "interaction.objects": "interaction",
                "interaction.animals": "interaction",
                "interaction.actions": "interaction",
                "interaction.observed_interactions": "interaction",
                "importance.potential_uses": "importance",
                "technical_details.implementation_steps": "technical_details",
                "technical_details.tools_and_technologies": "technical_details",
                "technical_details.example_projects": "technical_details",
                "technical_details.best_practices": "technical_details",
                "technical_details.common_challenges": "technical_details",
                "technical_details.debugging_tips": "technical_details",
                "technical_details.related_concepts": "technical_details",
                "technical_details.resources": "technical_details",
                "technical_details.code_examples": "technical_details"
            }
            print("Extracting entries from JSON data...")
            for key, value in response_data.items():
                entry = defaultdict(list)
                if key in single_value_fields:
                    print(f"Processing single value field: {key}")
                    field_name = key.split('.')[-1]
                    section = single_value_fields[key]
                    if not isinstance(section, list):
                        section = [section]
                    try:
                        entry[section[0]][field_name] = value if not isinstance(value, list) else (
                            value[0] if value else ""
                        )
                    except IndexError as e:
                        print(f"Error accessing field: {key}. Details: {e}")
                    except Exception as e:
                        print(f"Unexpected error processing single value field '{key}': {e}")
                elif key in list_type_fields:
                    print(f"Processing list type field: {key}")
                    field_name = key.split('.')[-1]
                    section = list_type_fields[key]
                    try:
                        entry[section][field_name].extend(value if isinstance(value, list) else [value])
                    except Exception as e:
                        print(f"Unexpected error processing list type field '{key}': {e}")
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
    global MEMORY_FRAME_NUMBER, EDIT_NUMBER
    print(f"\n{YELLOW}--- Storing Memory Frame ---{RESET}")
    connection_map = {}
    memories_folder_path = Get_path_of_memories_folder()
    memory_frame_paths = []

    try:
        script_path = os.path.abspath(os.path.dirname(__file__))
        connection_map_path = os.path.join(script_path, "memories", "Memory_connections_map.txt")
        with open(connection_map_path, 'r') as file:
            content = file.read()
            folder_matches = re.findall(r'\*\*\*\*(.*?)\*\*\*\*(.*?)Path:\s*(.*?)\n', content, re.DOTALL)
            for match in folder_matches:
                folder_name, folder_info, folder_path = match
                connection_map[folder_name.strip()] = folder_path.strip()
    except FileNotFoundError:
        print("Error: Connection map file not found.")

    storage_folders = memory_data.get("storage", {}).get("memory_folders_storage", [])
    print(f"Suggested storage folders: {storage_folders}")
    timestamp = datetime.now().strftime(TIMESTAMP_FORMAT)
    proposed_name = memory_data.get("naming_suggestion", {}).get("memory_frame_name", "UnnamedMemory")
    importance = memory_data.get("importance", {}).get("importance_level", "UnknownImportance")

    for folder_info in storage_folders:
        folder_path = folder_info.get("folder_path", "")
        probability = folder_info.get("probability", 0)
        print(f"Processing folder: {folder_path} (Probability: {probability})")
        if folder_path in connection_map:
            print(f"Folder '{folder_path}' found in connection map.")
            target_folder_path = connection_map[folder_path]
        else:
            print(f"Folder '{folder_path}' not in connection map. Creating in 'NewGeneratedbyAI'...")
            target_folder_path = os.path.join(script_path, "memories", "NewGeneratedbyAI", folder_path)
            os.makedirs(target_folder_path, exist_ok=True)
        highest_probability = max([folder.get("probability", 0) for folder in storage_folders], default=0)

        # Improved filename structure
        memory_frame_name = f"{proposed_name}_MemoryFrame_{MEMORY_FRAME_NUMBER:05d}_{timestamp}_Probability_{highest_probability}_Importance_{importance}.json"
        memory_frame_path = os.path.join(target_folder_path, memory_frame_name)
        print(f"Memory frame name: {memory_frame_name}")
        print(f"Memory frame path: {memory_frame_path}")
        memory_frame_data = {
            "input": user_input,
            "response1": response1_text,
            "response2": response2_text,
            "memory_data": memory_data,
            "timestamp": timestamp,
            "edit_number": EDIT_NUMBER
            # ... (Add other fields as needed) ...
        }
        try:
            with open(memory_frame_path, 'w') as file:
                json.dump(memory_frame_data, file, indent=4)
            print(f"{YELLOW}Memory frame saved successfully at: {memory_frame_path}{RESET}")
            memory_frame_paths.append(memory_frame_path)
        except Exception as e:
            print(f"Error saving memory frame: {e}")

    update_html_logs(MEMORY_FRAME_NUMBER, proposed_name, timestamp, memory_frame_paths, memories_folder_path)

    MEMORY_FRAME_NUMBER += 1
    EDIT_NUMBER = 0




def CREATE_MEMORY_FRAME____(conversationInput = "None"):
    MEMORY_FRAME_NUMBER = 1
    TIMESTAMP_FORMAT = '%Y-%m-%d_%H-%M'
    timestamp = datetime.now().strftime(TIMESTAMP_FORMAT)
    EDIT_NUMBER = 0


    MemorySumarisation = call_memory_model(user_input, conversationInput)
    memory_entries = extract_entries_smart(MemorySumarisation.text)
    for entry in memory_entries:
        store_memory_frame(user_input="None", response1_text=conversationInput, response2_text=MemorySumarisation, memory_data=entry)

while True:
    user_input = process_user_input()
    timestamp = datetime.now().strftime(TIMESTAMP_FORMAT)
    response1 = call_interaction_model(user_input, timestamp)
    if response1:
        response2 = call_memory_model(user_input, response1.text)
        if response2:
            memory_entries = extract_entries_smart(response2.text)
            for entry in memory_entries:
                store_memory_frame(user_input, response1.text, response2.text, entry)



