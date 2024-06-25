import google.generativeai as genai
import os
import re
import json
import pathlib
from datetime import datetime

# ANSI color codes for terminal output
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

# Memory frame and edit tracking
MEMORY_FRAME_NUMBER = 1
EDIT_NUMBER = 0
TIMESTAMP_FORMAT = '%Y-%m-%d_%H-%M'

# Configuration for Google Generative AI
genai.configure(api_key='AIzaSyA60tGw6fZwQdamW8sm6pkgRh5W559kLJ0')   # Replace with your actual API key

def sanitize_filename(filename):
    """Sanitize the filename for Windows compatibility."""
    return re.sub(r'[<>:"/\\|?*]', '_', filename)

def sanitize_href(href):
    """Sanitizes a given href string by replacing spaces with %20."""
    return href.replace(" ", "%20")


def update_html_logs(memory_frame_number, proposed_name, timestamp, memory_frame_paths, memories_folder_path):
    """Updates the HTML log file with correct absolute paths for href links."""
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
            href = sanitize_href(relative_path)
            html_insertion += f"""
                <li><a href='{href}'>{os.path.basename(href)}</a></li>
            """

        html_insertion += "</ul>"

        with open(log_file_path, 'a') as log_file:
            log_file.write(html_insertion)

        print(f"{GREEN}HTML logs updated successfully.{RESET}")
    except Exception as e:
        print(f"{RED}Error updating HTML logs: {e}{RESET}")
def get_path_of_memories_folder():
    """Returns the absolute path to the 'memories' folder."""
    current = pathlib.Path.cwd()
    memories_path = current / "memories"
    return memories_path.absolute()

def process_user_input():
    """Processes user input from the terminal."""
    user_input = input(f"{GREEN}Enter input: {RESET}")
    print(f"{MAGENTA}User input received: {user_input}{RESET}")
    return user_input


def call_interaction_model(user_input, timestamp):
    """Calls the interaction model and gets the response."""
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
        print(f"{RED}Error in Interaction Model: {e}{RESET}")
        return None


def call_memory_model(user_input, introspection, reflection, action, function_call_result, emotions, learning):
    """Calls the memory model and gets the structured response."""
    print(f"\n{CYAN}            ***------- Calling Memory Model (Loop MemoryFrame creation)------***{RESET}")
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
        create_memory_prompt = (f"User: {user_input}\n"
                                f"AI: {introspection}\n"
                                f"AI: {reflection}\n"
                                f"AI: {action}\n"
                                f"AI: {function_call_result}\n"
                                f"AI: {emotions}\n"
                                f"AI: {learning}\n"
                                )
        response = chat.send_message(create_memory_prompt)
        print(f"Memory Model Response:\n{response.text}")
        return response
    except Exception as e:
        print(f"{RED}Error in Memory Model: {e}{RESET}")
        return None


def extract_entries_smart(response_message):
    """Extracts structured entries from the response message."""
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

            if isinstance(response_data, list):
                for entry in response_data:
                    entries.append(entry)
            elif isinstance(response_data, dict):
                entries.append(response_data)
            else:
                print(f"{YELLOW}Warning: Unexpected data type: {type(response_data)}{RESET}")
                print("Skipping data.")
        except json.JSONDecodeError:
            print(f"{RED}Error: Invalid JSON in the AI response.{RESET}")
        except Exception as e:
            print(f"{RED}Error extracting entry: {e}{RESET}")
    return entries


def store_memory_frame(user_input, introspection, reflection, action, function_call_result, emotions, learning,
                       memory_data, session_info):
    """Stores a memory frame based on provided information and updates the HTML logs."""
    global MEMORY_FRAME_NUMBER, EDIT_NUMBER

    # Create filename for MemoryFrame
    timestamp = datetime.now().strftime(TIMESTAMP_FORMAT)
    importance = int(memory_data['importance']['importance_level'])
    suggested_name = memory_data['naming_suggestion']['memory_frame_name']

    # Sanitize the suggested name
    sanitized_name = sanitize_filename(suggested_name)

    filename = f"MemoryFrame___{session_info}___{timestamp}___importance___{importance:03d}___{sanitized_name}.json"

    # Construct the path
    base_path = get_path_of_memories_folder()

    # Get the suggested folder paths
    suggested_paths = memory_data['storage']['memory_folders_storage']

    # Sort suggested paths by probability (highest first)
    suggested_paths.sort(key=lambda x: x['probability'], reverse=True)

    # Use the path with the highest probability
    chosen_path = suggested_paths[0]['folder_path']

    # Split the path into individual folder names
    folder_names = chosen_path.split('/')

    # Construct the full path
    full_path = os.path.join(base_path, "AiGenerated", *folder_names)

    # Ensure the directory exists
    os.makedirs(full_path, exist_ok=True)

    # Construct full file path
    file_path = os.path.join(full_path, filename)

    # Construct memory frame content
    memory_frame_content = {
        "user_input": user_input,
        "introspection": introspection,
        "reflection": reflection,
        "action": action,
        "function_call_result": function_call_result,
        "emotions": emotions,
        "learning": learning,
        "memory_data": memory_data,
        "session_info": session_info
    }

    # Write the memory frame to a JSON file
    try:
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(memory_frame_content, f, indent=2, ensure_ascii=False)
        print(f"{YELLOW}--- Memory Frame Stored Successfully ---{RESET}")
        print(f"Stored at: {file_path}")

        # Update HTML logs
        update_html_logs(MEMORY_FRAME_NUMBER, suggested_name, timestamp, [file_path], base_path)
        MEMORY_FRAME_NUMBER += 1
    except Exception as e:
        print(f"{RED}Error writing Memory Frame: {e}{RESET}")


def CREATE_MEMORY_FRAME(user_input, introspection, reflection, action, function_call_result, emotions, learning,
                        session_info=None):
    """Main function to create a memory frame from user input and AI responses."""
    try:
        print("Calling memory model")
        memory_summary = call_memory_model(user_input=user_input, introspection=introspection, reflection=reflection,
                                           action=action, function_call_result=function_call_result, emotions=emotions,
                                           learning=learning)

        if memory_summary and hasattr(memory_summary, 'text'):
            print("Extracting memory entries")
            memory_entries = extract_entries_smart(memory_summary.text)

            if memory_entries:
                for entry in memory_entries:
                    store_memory_frame(user_input=user_input, introspection=introspection, reflection=reflection,
                                       action=action, function_call_result=function_call_result, emotions=emotions,
                                       learning=learning, memory_data=entry, session_info=session_info)
                print(f"{GREEN}Memory frame(s) stored successfully.{RESET}")
            else:
                print(f"{YELLOW}No valid memory entries found. Memory frame not stored.{RESET}")
        else:
            print(f"{YELLOW}No valid response from memory model. Memory frame not stored.{RESET}")
    except Exception as e:
        print(f"{RED}Error in CREATE_MEMORY_FRAME: {e}{RESET}")

    print(f"{GREEN}CREATE_MEMORY_FRAME FINISHED{RESET}")
"""  
if __name__ == "__main__":
    while True:
        user_input = process_user_input()
        timestamp = datetime.now().strftime(TIMESTAMP_FORMAT)
        response1 = call_interaction_model(user_input, timestamp)
        if response1:
            introspection = "example introspection"
            reflection = "example reflection"
            action = "example action"
            function_call_result = "example function call result"
            emotions = "example emotions"
            learning = "example learning"
            CREATE_MEMORY_FRAME(user_input, introspection, reflection, action, function_call_result, emotions, learning)"""