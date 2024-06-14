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
    memories_folder = os.path.join(script_path, "memories")

    # Check if 'memories' folder exists, recreate if not
    if not os.path.exists(memories_folder):
        print(f"Creating 'memories' folder: {memories_folder}")
        os.makedirs(memories_folder, exist_ok=True)
        print_colored("Folder structure recreated!", "green")
        create_folder_structure(memory_templates)
    else:
        print(f"'memories' folder exists. Checking for files...")

    # Check for connection map and folder structure files
    connection_map_file = os.path.join(memories_folder, "Memory_connecions_map.txt")
    folder_structure_file = os.path.join(memories_folder, "directory_structure.txt")

    # Check if connection map file is missing
    if not os.path.exists(connection_map_file):
        print(f"Connection map file missing: {connection_map_file}")
        create_connection_map(memories_folder)
        print_colored("Connection map recreated!", "green")

    # Check if folder structure file is missing
    if not os.path.exists(folder_structure_file):
        print(f"Folder structure file missing: {folder_structure_file}")
        create_folder_structure(memory_templates)
        create_connection_map(memories_folder)
        print_colored("Folder structure and connection map recreated!", "green")

    # Check if current folder structure file is missing
    current_folder_structure_file = os.path.join(memories_folder, "current_folder_structure.txt")
    if not os.path.exists(current_folder_structure_file):
        print(f"Current folder structure file missing: {current_folder_structure_file}")
        summarise_memory_folder_structure(memories_folder, file_path=current_folder_structure_file)
        print_colored("Current folder structure file recreated!", "green")


def create_connection_map(base_folder):
    """Creates a connection map file with similar folder names and paths."""
    folder_list = []
    for root, dirs, files in os.walk(base_folder):
        for dir_name in dirs:
            folder_path = os.path.join(root, dir_name)
            folder_list.append((dir_name, folder_path))

    similar_folders = find_similar_folders(folder_list)

    with open(os.path.join(base_folder, "Memory_connecions_map.txt"), "w") as f:
        for folder_name, paths in similar_folders.items():
            f.write(f"**** {folder_name} ****\n")  # Add separator
            for path in paths:
                f.write(f"  Path: {path}\n")
            f.write("\n")


def create_folder_structure(memory_templates):
    """Creates the folder structure based on the memory templates."""
    script_path = os.path.abspath(os.path.dirname(__file__))
    folder_list = []

    for template_name, template_data in memory_templates.items():
        print(f"Processing template: {template_name}")

        template_name_safe = template_name.replace(":", "_")
        print(f"  Safe template name: {template_name_safe}")

        base_folder = os.path.join(script_path, "memories")
        print(f"  Creating template folder: {base_folder}")
        os.makedirs(base_folder, exist_ok=True)
        folder_list.append((template_name_safe, base_folder))

        template_folder = os.path.join(base_folder, template_name_safe)
        print(f"  Creating template folder: {template_folder}")
        os.makedirs(template_folder, exist_ok=True)
        folder_list.append((template_name_safe, template_folder))

        create_folders_from_structure(template_data["structure"], template_folder, folder_list)

    # Create connection map
    create_connection_map(base_folder)








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


if __name__ == "__main__":
    create_file_structure(memory_templates)