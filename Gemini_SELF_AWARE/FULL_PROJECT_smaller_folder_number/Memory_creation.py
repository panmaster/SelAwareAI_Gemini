from collections import defaultdict
from datetime import datetime
memory_templates = {
    "CoreMemory": {
        "structure": {
            "Core Experiences": {
                "Significant Moments": {
                    "Personal": [],
                    "Professional": [],
                    "Travel": [],
                    "Other": []
                },
                "Life-Changing Events": {
                    "Positive": [],
                    "Negative": []
                },
                "Turning Points": {
                    "In Relationships": [],
                    "In Career": [],
                    "In Personal Growth": [],
                    "Other": []
                },
                "Challenges Faced": {
                    "Internal Challenges": {
                        "Fear & Anxiety": {
                            "Specific Fears": [],
                            "How I Coped": [],
                            "What I Learned": []
                        },
                        "Self-Doubt": {
                            "Sources of Self-Doubt": [],
                            "How I Overcame It": [],
                            "What I Learned": []
                        },
                        "Negative Thought Patterns": {
                            "Common Negative Thoughts": [],
                            "Strategies for Changing Them": [],
                            "What I Learned": []
                        }
                    },
                    "External Challenges": {
                        "Obstacles": {
                            "Types of Obstacles": [],
                            "How I Overcame Them": [],
                            "What I Learned": []
                        },
                        "Setbacks": {
                            "Types of Setbacks": [],
                            "How I Recovered": [],
                            "What I Learned": []
                        }
                    }
                },
                "Triumphs & Accomplishments": {
                    "Personal Achievements": {
                        "Goals Achieved": [],
                        "Personal Growth": [],
                        "Impact on Life": []
                    },
                    "Professional Successes": {
                        "Projects & Achievements": [],
                        "Career Growth": [],
                        "Impact on Life": []
                    },
                    "Creative Wins": {
                        "Creative Works": [],
                        "Recognition & Awards": [],
                        "Impact on Life": []
                    }
                }
            },
            "Relationships": {
                "Family": {
                    "Parents": {
                        "Memorable Moments": [],
                        "Challenges Faced": [],
                        "Lessons Learned": [],
                        "Impact on My Life": []
                    },
                    "Siblings": {
                        "Memorable Moments": [],
                        "Challenges Faced": [],
                        "Lessons Learned": [],
                        "Impact on My Life": []
                    },
                    "Extended Family": {
                        "Memorable Moments": [],
                        "Challenges Faced": [],
                        "Lessons Learned": [],
                        "Impact on My Life": []
                    }
                },
                "Friendships": {
                    "Close Friends": {
                        "Memorable Moments": [],
                        "Challenges Faced": [],
                        "Lessons Learned": [],
                        "Impact on My Life": []
                    },
                    "Circles & Groups": {
                        "Shared Experiences": [],
                        "Impact on My Life": [],
                        "Lessons Learned": []
                    },
                    "Meaningful Interactions": {
                        "Unexpected Encounters": [],
                        "Impact on My Life": [],
                        "Lessons Learned": []
                    }
                },
                "Romantic Relationships": {
                    "Partners": {
                        "Memorable Moments": [],
                        "Challenges Faced": [],
                        "Lessons Learned": [],
                        "Impact on My Life": []
                    },
                    "Relationship Milestones": {
                        "First Date": [],
                        "First Kiss": [],
                        "Moving In Together": [],
                        "Marriage": [],
                        "Other Milestones": []
                    }
                }
            },
            "Reflections & Insights": {
                "Lessons Learned": {
                    "From Successes": [],
                    "From Mistakes": [],
                    "From Relationships": []
                },
                "Self-Discovery": {
                    "Strengths & Talents": [],
                    "Areas for Growth": [],
                    "What I've Learned About Myself": []
                }
            },
            "Goals & Visions": {
                "Life Vision": {
                    "Short-Term Goals": [],
                    "Mid-Term Goals": [],
                    "Long-Term Goals": []
                },
                "Personal Goals": {
                    "Short-Term Goals": [],
                    "Mid-Term Goals": [],
                    "Long-Term Goals": []
                }
            },
            "Knowledge Base": {
                "Key Concepts & Theories": [],
                "Areas of Expertise": [],
                "Personal Beliefs & Values": []
            },
            "Conceptual Exploration": {
                "Paradoxes & Contradictions": [],
                "Unknowns & Mysteries": [],
                "Contradictions & Dilemmas": []
            }
        }
    },
    "Actions & Results": {
        "structure": {
            "Actions & Results": {
                "Past": {
                    "Actions I Took": [],
                    "Results Achieved": [],
                    "Lessons Learned": []
                },
                "Present": {
                    "Current Actions": [],
                    "Expected Outcomes": [],
                    "Potential Challenges": []
                },
                "Future": {
                    "Planned Actions": [],
                    "Anticipated Results": [],
                    "Potential Obstacles": []
                }
            }
        }
    },
    "Emotional Landscape": {
        "structure": {
            "Dominant Emotions": ["Joy", "Sadness", "Anger", "Fear", "Love", "Other"],
            "Emotional Triggers": {
                "Situations": [],
                "People": [],
                "Thoughts": [],
                "Physical Sensations": []
            }
        }
    },
    "Planning & Progress": {
        "structure": {
            "Plans & Strategies": {
                "Short-Term Plans": [],
                "Long-Term Plans": [],
                "Strategies Used": {
                    "Time Management": [],
                    "Goal Setting": [],
                    "Problem Solving": [],
                    "Other Strategies": []
                }
            },
            "Progress & Outcomes": {
                "Goals Achieved": [],
                "Goals Not Achieved": [],
                "Lessons Learned from Progress": [],
                "Results of Actions": {
                    "Positive Results": [],
                    "Negative Results": []
                }
            }
        }
    },
    "Life Events & Transitions": {
        "structure": {
            "Significant Events": {
                "Personal": {
                    "Birthdays": [],
                    "Graduations": [],
                    "Weddings": [],
                    "Other Personal Events": []
                },
                "Professional": {
                    "Job Changes": [],
                    "Promotions": [],
                    "Project Completions": [],
                    "Other Professional Events": []
                },
                "Travel": {
                    "Trips & Journeys": [],
                    "Moving Homes": [],
                    "Other Travel Events": []
                },
                "Other": []
            },
            "Life Transitions": {
                "Personal Growth": {
                    "Milestones": [],
                    "Challenges Overcome": [],
                    "Significant Decisions": []
                },
                "Relationships": {
                    "Family Dynamics": [],
                    "Friendships": [],
                    "Romantic Relationships": [],
                    "Professional Connections": []
                },
                "Health & Wellbeing": {
                    "Physical Health": [],
                    "Mental & Emotional Health": [],
                    "Habits & Routines": []
                },
                "Knowledge & Skills": {
                    "Formal Education": [],
                    "Self-Directed Learning": [],
                    "Skills & Expertise": []
                }
            }
        }
    },
    "Emotions & Reflections": {
        "structure": {
            "Emotional Experiences": {
                "Dominant Emotions": [
                    "Joy & Excitement",
                    "Love & Connection",
                    "Sadness & Grief",
                    "Anger & Frustration",
                    "Fear & Anxiety",
                    "Other Emotions"
                ],
                "Emotional Triggers": [
                    "Situations",
                    "People",
                    "Thoughts"
                ]
            },
            "Personal Growth & Insights": {
                "Lessons Learned": [
                    "From Successes",
                    "From Mistakes",
                    "From Relationships"
                ],
                "Self-Discovery": [
                    "Strengths & Talents",
                    "Areas for Growth",
                    "What I've Learned About Myself"
                ]
            }
        }
    },
    "Goals & Aspirations": {
        "structure": {
            "Personal Goals": {
                "Health & Wellbeing": [],
                "Personal Development": [],
                "Relationships": [],
                "Creative Pursuits": [],
                "Other Personal Goals": []
            },
            "Professional Goals": {
                "Career Advancement": [],
                "Skills & Expertise": [],
                "Project Goals": [],
                "Other Professional Goals": []
            },
            "Life Vision": {
                "Values & Beliefs": [],
                "Aspirations": [],
                "Dreams": []
            }
        }
    },
    "Challenges & Setbacks": {
        "structure": {
            "Significant Mistakes": {
                "Description": [],
                "Lessons Learned": [],
                "How I Grew": []
            },
            "Failures & Disappointments": {
                "In Personal Projects": [],
                "In Relationships": [],
                "In Career": []
            },
            "Difficult Emotions": {
                "Fear & Anxiety": [],
                "Anger & Frustration": [],
                "Sadness & Grief": [],
                "Shame & Guilt": [],
                "Jealousy & Envy": [],
                "Trauma & Abuse": {
                    "Experiences": [],
                    "Impact": [],
                    "Healing Journey": []
                }
            },
            "Negative Thought Patterns": [],
            "Areas for Improvement": []
        }
    },
    "Knowledge & Learning": {
        "structure": {
            "Formal Education": {
                "Schools": [],
                "Degrees & Certifications": [],
                "Significant Projects": []
            },
            "Self-Directed Learning": {
                "Skills Acquired": [],
                "Areas of Interest": [],
                "Learning Resources": {
                    "Bookshelf": [],
                    "Online Courses": [],
                    "Mentors & Teachers": []
                }
            },
            "Knowledge Base": {
                "Facts & Concepts": [],
                "Historical Events": [],
                "Scientific Discoveries": [],
                "Philosophical Ideas": [],
                "Artistic Movements": [],
                "Cultural Insights": []
            },
            "Laws & Regulations": {
                "Legal Knowledge": [],
                "Personal Experiences with Laws": [],
                "Understanding of Legal Systems": []
            }
        }
    },
    "Actions & Results": {
        "structure": {
            "Actions & Results": {
                "Past": [],
                "Present": [],
                "Future": []
            }
        }
    },
    "Emotional Landscape": {
        "structure": {
            "Dominant Emotions": [],
            "Emotional Triggers": []
        }
    },
    "Planning & Progress": {
        "structure": {
            "Plans & Strategies": {
                "Short-Term Plans": [],
                "Long-Term Plans": [],
                "Strategies Used": {
                    "Time Management": [],
                    "Goal Setting": [],
                    "Problem Solving": [],
                    "Other Strategies": []
                }
            },
            "Progress & Outcomes": {
                "Goals Achieved": [],
                "Goals Not Achieved": [],
                "Lessons Learned from Progress": [],
                "Results of Actions": {
                    "Positive Results": [],
                    "Negative Results": []
                }
            }
        }
    }
}


import google.generativeai as genai
import re
import os
import json
from datetime import datetime
from fuzzywuzzy import fuzz  # Import fuzzywuzzy for fuzzy string matching


# ANSI color codes for terminal output
class TerminalColors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

    # Define color codes as dictionary
    COLOR_CODES = {
        "red": FAIL,
        "green": OKGREEN,
        "yellow": WARNING,
        "blue": OKBLUE,
        "magenta": HEADER,

        "reset": ENDC
    }


# Configure the GenAI API
genai.configure(api_key='AIzaSyCltjPhJwWRL3BufxCdz-B4mc-6QdmQKBs')


def print_colored(text, color="white"):
    """Prints text with the specified color."""
    print(f"{TerminalColors.COLOR_CODES.get(color, '')}{text}{TerminalColors.COLOR_CODES['reset']}")


def create_folders_from_structure(structure, base_folder, folder_list):
    """Creates folders from the given structure."""
    for level1_key in structure:
        print(f"    Creating level 1 folder: {level1_key}")
        level1_folder = os.path.join(base_folder, level1_key)
        os.makedirs(level1_folder, exist_ok=True)
        folder_list.append((level1_key, level1_folder))
        print(f"      Added folder {level1_key} to list: {level1_folder}")

        if isinstance(structure[level1_key], dict):
            print(f"      Found nested dictionary for {level1_key}")
            create_folders_from_structure(structure[level1_key], level1_folder, folder_list)

def find_similar_folders(folder_list):
    """Finds similar folder names in the list using Levenshtein distance."""
    similar_folders = {}

    total_comparisons = len(folder_list) * (len(folder_list) - 1) // 2  # Calculate total comparisons
    comparisons_left = total_comparisons

    for i in range(len(folder_list)):
        folder_name_1, path_1 = folder_list[i]

        if folder_name_1 not in similar_folders:
            similar_folders[folder_name_1] = [path_1]

        for j in range(i + 1, len(folder_list)):
            folder_name_2, path_2 = folder_list[j]

            similarity_score = fuzz.ratio(folder_name_1, folder_name_2)

            print(f"Comparing '{folder_name_1}' and '{folder_name_2}': Score = {similarity_score}")
            print_colored(f"Porównań pozostało: {comparisons_left}", "yellow") # Print remaining comparisons in yellow
            comparisons_left -= 1

            # Adjust threshold as needed
            if similarity_score >= 80:  # Example threshold adjusted to 80
                print(f"   Found similar folders: '{folder_name_1}' and '{folder_name_2}'")
                if folder_name_1 in similar_folders:
                    similar_folders[folder_name_1].append(path_2)
                else:
                    similar_folders[folder_name_1] = [path_1, path_2]

    return similar_folders

def compare_folder_names(name1, name2):
    """Funkcja porównuje dwie nazwy folderów, ignorując wielkość liter."""
    name1 = name1.lower()
    name2 = name2.lower()

    # Obliczenie długości wspólnego prefiksu
    common_prefix_length = 0
    for i in range(min(len(name1), len(name2))):
        print(f"Comapring    {name1}     and    {name2}  ")
        if name1[i] == name2[i]:
            common_prefix_length += 1
        else:
            break


    # Zwrócenie procentu podobieństwa
    return common_prefix_length / max(len(name1), len(name2))



def create_file_structure(memory_templates):
    """Creates the file structure for storing memories based on the provided templates."""
    script_path = os.path.abspath(os.path.dirname(__file__))
    folder_list = []  # List to store folder names and paths

    for template_name, template_data in memory_templates.items():
        print(f"Processing template: {template_name}")

        template_name_safe = template_name.replace(":", "_")
        print(f"  Safe template name: {template_name_safe}")

        base_folder = os.path.join(script_path, "memories")
        print(f"  Creating base folder: {base_folder}")
        os.makedirs(base_folder, exist_ok=True)
        folder_list.append((template_name_safe, base_folder))

        template_folder = os.path.join(base_folder, template_name_safe)
        print(f"  Creating template folder: {template_folder}")
        os.makedirs(template_folder, exist_ok=True)
        folder_list.append((template_name_safe, template_folder))

        create_folders_from_structure(template_data["structure"], template_folder, folder_list)

    # Compare folder names and create connection map
    similar_folders = find_similar_folders(folder_list)

    # Save connection map to "Memory_connecions_map.txt"
    with open("memories/Memory_connecions_map.txt", "w") as f:
        for folder_name, paths in similar_folders.items():
            f.write(f"**** {folder_name} ****\n")  # Add separator
            for path in paths:
                f.write(f"  Path: {path}\n")
            f.write("\n")
reconstruct = str(input("reconstruct??"))

if reconstruct ==  "reconstruct":
    create_file_structure(memory_templates)





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
            print("checking")
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


def retrieve_memories(phrase, log_filepath):
    """Retrieves memory frames based on phrase matching, folder traversal, and temporal sorting."""
    phrase_parts = re.findall(r'\w+', phrase)  # Example: simple word splitting
    candidate_frames = []

    for root, _, files in os.walk("memories"):
        for file in files:
            if file.endswith(".json"):
                filepath = os.path.join(root, file)
                for part in phrase_parts:
                    if part.lower() in filepath.lower():
                        # Load the memory frame from the file
                        with open(filepath, 'r') as f:
                            frame_data = json.load(f)
                            frame_data["Path"] = filepath  # Add filepath to data
                            candidate_frames.append(frame_data)
                        break  # Move to next file after finding a match

    # Sort by timestamp and group by session
    sorted_frames = sorted(candidate_frames, key=lambda x: x["Time"], reverse=True)
    sessions = {}
    for frame in sorted_frames:
        session_id = frame["Session"]
        if session_id not in sessions:
            sessions[session_id] = []
        sessions[session_id].append(frame)

    # Create sets of frames based on the session and time
    all_frames = sorted_frames  # All frames, sorted by time

    # Example: Create a contextual set of frames
    contextual_sets = {}  # Store multiple contextual sets
    for session_id, frames in sessions.items():
        for i, frame in enumerate(frames):
            contextual_set = []
            contextual_set.append(frame)

            # Add frames before the current frame
            for j in range(i - 1, -1, -1):
                contextual_set.append(frames[j])

            # Add frames after the current frame
            for j in range(i + 1, len(frames)):
                contextual_set.append(frames[j])

            contextual_sets[f"{session_id}_{frame['Time']}"] = contextual_set



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
    except Exception as E:
        print(E)
    if outcome is None:
        outcome = ""
    return outcome


FUNCTION_MAPPING = {
    # Example:
    # "play_music": play_music,
}

def STORE_MEMORY_Frame(current_time, user_input, ai_response, ai_response2, memory_data):
    """Stores structured memory data and the conversation frame across multiple templates SIMULTANEOUSLY."""
    # Define color codes
    red = "\033[91m"
    green = "\033[92m"
    yellow = "\033[93m"
    blue = "\033[94m"
    magenta = "\033[95m"
    cyan = "\033[96m"
    white = "\033[97m"
    reset = "\033[0m"
    import json
    from collections import defaultdict
    from typing import List, Dict

    # --- Load Connection Map ---
    script_path = os.path.abspath(os.path.dirname(__file__))
    connection_map_path = os.path.join(script_path, "memories", "Memory_connecions_map.txt")
    with open(connection_map_path, 'r', encoding='utf-8') as f:
        connection_map_data = f.read()

    # --- Process Connection Map Data ---
    connection_map = defaultdict(list)
    for line in connection_map_data.splitlines():
        if "****" in line:
            current_folder_name = line.strip("****").strip()
        elif "  Path:" in line:
            path = line.strip("  Path:").strip()
            connection_map[current_folder_name].append(path)

    print(f"{yellow}Connection Map: {connection_map}{reset}")

    def extract_entries_smart(response_message):

        entries = []
        print(f"{magenta}extract_entries_smart{reset}")

        # Use regex to find the JSON block
        json_match = re.search(r"```json\n(.*?)\n```", response_message, re.DOTALL)

        # If JSON block is found, extract the JSON data
        if json_match:
            try:
                json_data = json_match.group(1)  # Extract JSON string
                response_data = json.loads(json_data)
                print(f"{green}Successfully loaded JSON data:{reset}")
                print(json.dumps(response_data, indent=4))  # Print the loaded JSON data

                # --- Extract data using matching rules ---
                entry = defaultdict(list)

                # Define a set of single-value fields
                single_value_fields = {
                    "concise_summary",
                    "main_topic",
                    "problem_solved",
                    "concept_definition",
                    "category",
                    "subcategory",
                    "memory_about",
                    "interaction_type",  # Handle potential lists
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

                # Define a set of list-type fields
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
                    "implementation_steps",  # Handle lists of dictionaries
                    "resources",  # Handle lists of dictionaries
                    "code_examples"  # Handle lists of dictionaries
                }

                # Direct Matching:
                for key, value in response_data.items():
                    if key in single_value_fields:
                        if isinstance(value, list):
                            entry[key].extend(value)  # Handle potential list values
                        else:
                            entry[key] = value
                        print(f"{blue}Direct match: {key} = {value}{reset}")
                    elif key in list_type_fields:
                        if isinstance(value, list):
                            if value and isinstance(value[0], dict):
                                entry[key].extend(value)  # Handle lists of dictionaries
                            else:
                                entry[key].extend(value)  # Handle lists of simple values
                        else:
                            entry[key].append(value)  # Handle single value
                        print(f"{blue}List match: {key} = {value}{reset}")

                # Keyword-Based Mapping:
                for key, value in response_data.items():
                    if "keyword" in key.lower() and isinstance(value, list):
                        entry["keywords"].extend(value)
                        print(f"{blue}Keyword match: {key} = {value}{reset}")
                    elif "description" in key.lower():
                        entry["description"] = value
                        print(f"{blue}Description match: {key} = {value}{reset}")
                    elif "summary" in key.lower():
                        entry["concise_summary"] = value
                        print(f"{blue}Summary match: {key} = {value}{reset}")
                    elif "step" in key.lower() and isinstance(value, list) and value and isinstance(value[0], dict):
                        entry["implementation_steps"].extend(value)
                        print(f"{blue}Step match: {key} = {value}{reset}")
                    elif "resource" in key.lower() and isinstance(value, list) and value and isinstance(value[0], dict):
                        entry["resources"].extend(value)
                        print(f"{blue}Resource match: {key} = {value}{reset}")
                    elif "code" in key.lower() and isinstance(value, list) and value and isinstance(value[0], dict):
                        entry["code_examples"].extend(value)
                        print(f"{blue}Code match: {key} = {value}{reset}")

                # Additional Matching:
                for key, value in response_data.items():
                    if "interaction_type" in key.lower() and isinstance(value, list):
                        entry["interaction_type"].extend(value)
                        print(f"{blue}Interaction type match: {key} = {value}{reset}")
                    elif "category" in key.lower():
                        entry["category"] = value
                        print(f"{blue}Category match: {key} = {value}{reset}")
                    elif "subcategory" in key.lower():
                        entry["subcategory"] = value
                        print(f"{blue}Subcategory match: {key} = {value}{reset}")

                # --- Store 'storage' information ---
                entry["storage"] = {
                    "storage_method": "",  # Placeholder - You might extract this from the AI response
                    "location": "",  # Placeholder - You might extract this from the AI response
                    "memory_folders_storage": [],  # These will be set later
                    "strenght of matching memory to given folder": []  # These will be set later
                }

                # Append the entry to the list
                entries.append(dict(entry))  # Convert back to regular dict
                print(f"{green}Extracted entry: {entry}{reset}")  # Print the extracted entry
                print(f"{yellow}{'-' * 30}{reset}")  # Separator for better readability

            except json.JSONDecodeError:
                print(f"{red}Error: Invalid JSON in response message.{reset}")
            except Exception as e:
                print(f"{red}Error extracting entry: {e}{reset}")

        return entries

    extracted_entries = extract_entries_smart(ai_response2)

    if extracted_entries:
        # --- Analyze and Categorize ---
        for entry in extracted_entries:
            print(f"{yellow}Analyzing entry: {entry}{reset}")
            # --- Find Matching Folders ---
            matching_folders = []
            print(f"{magenta}Matching Folders: {matching_folders}{reset}")

            category, time_period, keyword = categorize_memory(entry["concise_summary"], connection_map)

            if category and time_period:
                print(f"{green}Memory categorized as {category} - {time_period} - {keyword}{reset}")
                # Retrieve potential folders for the memory based on the connection map
                matching_folders = connection_map.get(f"{category} - {time_period}", [])
            else:
                print(f"{yellow}Memory categorization: Uncategorized, Unknown, Unknown{reset}")

            if matching_folders:
                print(f"{green}Matching Folders found: {matching_folders}{reset}")

                # --- Calculate matching scores ---
                matching_scores = []
                for folder in matching_folders:
                    # Extract category and time_period from the folder name
                    parts = folder.split("\\")[-2:]  # Get last two parts of the path
                    category = parts[0]
                    time_period = parts[1]

                    # Calculate similarity scores
                    similarity_score = fuzz.ratio(entry["concise_summary"], f"{category} {time_period}")
                    matching_scores.append((folder, similarity_score))

                # --- Update memory frame ---
                entry["storage"]["memory_folders_storage"] = matching_folders
                entry["storage"]["strenght of matching memory to given folder"] = matching_scores
                print(f"{green}Updated memory frame: {entry}{reset}")

                # --- Store Memory Frame ---
                script_path = os.path.abspath(os.path.dirname(__file__))
                memory_frame_number = memory_data.get('MEMORY_FRAME_NUMBER', 1)
                edit_number = memory_data.get('EDIT_NUMBER', 0)
                timestamp_format = "%Y-%m-%d_%H-%M-%S"
                timestamp = current_time.strftime(timestamp_format)
                for folder, similarity_score in matching_scores:  # Iterate using folder and score
                    # Add strength score to file name if it's not "unknown"
                    file_name_suffix = ""
                    if similarity_score != "unknown":
                        file_name_suffix = f"_strenght_{similarity_score}"

                    memory_frame_filepath = os.path.join(script_path, folder,
                                                         f"MemoryFrame_{memory_frame_number}_{edit_number}_{timestamp}{file_name_suffix}.json")
                    os.makedirs(os.path.join(script_path, folder), exist_ok=True)
                    with open(memory_frame_filepath, "w") as f:
                        json.dump(entry, f, indent=4)

                    # --- Update Memory Frame Log ---
                    os.makedirs(os.path.join(script_path, "memory_logs"), exist_ok=True)
                    memory_log_filepath = os.path.join(script_path, "memory_logs", "MemoryFrames_log.txt")
                    with open(memory_log_filepath, 'a', encoding='utf-8') as f:
                        f.write(
                            f"MemoryFrame: {memory_frame_number}, Edit: {edit_number}, Type: JSON, path: {memory_frame_filepath}, time: {timestamp}, session: {memory_frame_number}_{edit_number}\n"
                        )  # Log the file path
                    print(f"Memory frame log updated: {memory_log_filepath}")
                    print(f"{green}Memory frame saved in: {memory_frame_filepath}{reset}")

            else:
                print(f"{yellow}No matching folders found for this memory frame{reset}")
    else:
        print(f"{yellow}No JSON data found in the AI response{reset}")

    # --- Store Conversation Frame ---
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
    print(f"Conversation frame saved in: {conversation_filepath}")

    # Increment memory frame number
    memory_data['MEMORY_FRAME_NUMBER'] += 1

    # --- Update Memory Frame Log ---
    os.makedirs(os.path.join(script_path, "memory_logs"), exist_ok=True)
    memory_log_filepath = os.path.join(script_path, "memory_logs", "MemoryFrames_log.txt")
    with open(memory_log_filepath, 'a', encoding='utf-8') as f:
        f.write(
            f"MemoryFrame: {memory_frame_number - 1}, Edit: {edit_number}, Type: Text, path: {memory_frame_filepath}, time: {timestamp}, session: {memory_frame_number - 1}_{edit_number}\n"
        )  # Log the file path
    print(f"Memory frame log updated: {memory_log_filepath}")


def summarise_memory_folder_structure(folder_path, file_path="directory_structure.txt", include_files=True):


    ignore_files = [".\\directory_structure.txt", ".\\Memory_connecions_map.txt"]

    with open(file_path, 'w') as f:
        f.write(f"Directory structure for: {folder_path}\n\n")
        for root, dirs, files in os.walk(folder_path):
            # Write folder path to file
            f.write(f"{root}\n")

            if include_files:
                # Write file names to file, ignoring specified files
                for file in files:
                    full_path = os.path.join(root, file)
                    if full_path not in ignore_files:
                        f.write(f"{full_path}\n")


# --- Create File Structure and Connection Map ---
create_file_structure(memory_templates)
directory_structure = summarise_memory_folder_structure(folder_path="./memories",
                                                        file_path="./memories/directory_structure.txt")
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
        prompt = f"currentTime:  {formatted_timestamp}  create {user_input} "
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
                    Provide the following information in a structured format using JSON:  you  have  2 Templates to choose form

                    you can also  cut  out entries  if  they  dont  seem  approparate for  memory storage and would be  empty
                    never  crose  out   "Memory Folder storage entry": 
                    """,

        )
        print(
            f" *****************************************************************************************************")
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

        print(create_memory_prompt)

        response2 = chat_2.send_message(create_memory_prompt)
        print("-----------------------------------------------------------------------------------")
        print(f"  Memory Data: {response2.text}")
        print(f"  ******---->STORE_MEMORY_Frame *******")

        # --- Function Execution ---
        response_interpreter_for_function_calling(response2)
        try:
            STORE_MEMORY_Frame(
                current_time,  # Pass current_time as the first argument
                user_input,
                response1.text,
                response2.text,
                memory_data
            )
        except Exception as e:
            print(e);

    except Exception as e:
        print_colored(f"Error in the main loop: {e}", "red")