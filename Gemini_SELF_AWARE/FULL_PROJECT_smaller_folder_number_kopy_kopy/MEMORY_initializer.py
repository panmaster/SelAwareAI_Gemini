import os
from collections import defaultdict
from fuzzywuzzy import fuzz
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


class TerminalColors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    COLOR_CODES = {
        "red": FAIL,
        "green": OKGREEN,
        "yellow": WARNING,
        "blue": OKBLUE,
        "magenta": HEADER,
        "reset": ENDC
    }

def print_colored(text, color="white"):
    print(f"{TerminalColors.COLOR_CODES.get(color, '')}{text}{TerminalColors.COLOR_CODES['reset']}")

def create_folders_from_structure(structure, base_folder, folder_list):
    for level1_key in structure:
        level1_folder = os.path.join(base_folder, level1_key)
        os.makedirs(level1_folder, exist_ok=True)
        folder_list.append((level1_key, level1_folder))
        if isinstance(structure[level1_key], dict):
            create_folders_from_structure(structure[level1_key], level1_folder, folder_list)

def find_similar_folders(folder_list):
    print_colored("Finding similar folders...", "blue")
    similar_folders = {}
    total_checks = 0
    executed_checks = 0
    total_possible_checks = len(folder_list) * (len(folder_list) - 1) // 2

    print_colored(f"  - Total folders: {len(folder_list)}", "blue")
    print_colored(f"  - Total possible checks: {total_possible_checks}", "blue")

    # First Pass: Token Sort Ratio (80% threshold)
    print_colored("First Pass: Checking for similar folders using Token Sort Ratio...", "blue")
    checks_remaining = total_possible_checks  # Initialize remaining checks
    for i in range(len(folder_list)):
        folder_name_1, path_1 = folder_list[i]
        if folder_name_1 not in similar_folders:
            similar_folders[folder_name_1] = [path_1]

        for j in range(i + 1, len(folder_list)):
            folder_name_2, path_2 = folder_list[j]

            similarity_score = fuzz.token_sort_ratio(folder_name_1, folder_name_2)

            # Print individual check details with remaining checks
            print_colored(
                f"  - Checking {total_checks+1}/{total_possible_checks} (Remaining: {checks_remaining-1}): '{folder_name_1}' against '{folder_name_2}': Similarity Score: {similarity_score}",
                "blue",
            )

            total_checks += 1
            checks_remaining -= 1  # Decrement remaining checks

            if similarity_score >= 80:
                executed_checks += 1
                print_colored(
                    f"    - Folders are similar (Token Sort Ratio >= 80%):  '{folder_name_1}' and '{folder_name_2}'",
                    "green",
                )
                similar_folders[folder_name_1].append(path_2)
            else:
                print_colored(
                    f"    - Folders are not similar (Token Sort Ratio < 80%):  '{folder_name_1}' and '{folder_name_2}'",
                    "yellow",
                )

    # Second Pass: Fuzzy Ratio (70% threshold)
    print_colored("Second Pass: Checking for similar folders using Fuzzy Ratio...", "blue")
    # DO NOT reset checks_remaining here - it should continue from the first pass
    for i in range(len(folder_list)):
        folder_name_1, path_1 = folder_list[i]
        if folder_name_1 not in similar_folders:
            similar_folders[folder_name_1] = [path_1]

        for j in range(i + 1, len(folder_list)):
            folder_name_2, path_2 = folder_list[j]

            similarity_score = fuzz.ratio(folder_name_1, folder_name_2)

            # Print individual check details with remaining checks
            print_colored(
                f"  - Checking {total_checks+1}/{total_possible_checks} (Remaining: {checks_remaining-1}): '{folder_name_1}' against '{folder_name_2}': Similarity Score: {similarity_score}",
                "blue",
            )

            total_checks += 1
            checks_remaining -= 1  # Decrement remaining checks

            if similarity_score >= 70:
                executed_checks += 1
                print_colored(
                    f"    - Folders are similar (Fuzzy Ratio >= 70%):  '{folder_name_1}' and '{folder_name_2}'",
                    "green",
                )
                similar_folders[folder_name_1].append(path_2)
            else:
                print_colored(
                    f"    - Folders are not similar (Fuzzy Ratio < 70%):  '{folder_name_1}' and '{folder_name_2}'",
                    "yellow",
                )

    print_colored(f"  - Total checks: {total_checks}", "blue")
    print_colored(f"  - Executed checks (Similarity Score >= 80% or Token Sort Ratio >= 70%): {executed_checks}", "blue")
    print_colored(f"  - Left: {total_checks - executed_checks}", "blue")
    return similar_folders

def create_file_structure(memory_templates):
    script_path = os.path.abspath(os.path.dirname(__file__))
    folder_list = []
    for template_name, template_data in memory_templates.items():
        template_name_safe = template_name.replace(":", "_")
        base_folder = os.path.join(script_path, "memories")
        os.makedirs(base_folder, exist_ok=True)
        folder_list.append((template_name_safe, base_folder))
        template_folder = os.path.join(base_folder, template_name_safe)
        os.makedirs(template_folder, exist_ok=True)
        folder_list.append((template_name_safe, template_folder))
        create_folders_from_structure(template_data["structure"], template_folder, folder_list)
    similar_folders = find_similar_folders(folder_list)
    with open("memories/Memory_connecions_map.txt", "w") as f:
        for folder_name, paths in similar_folders.items():
            f.write(f"**** {folder_name} ****\n")
            for path in paths:
                f.write(f"  Path: {path}\n")
            f.write("\n")

    # Add the code from the `else` block here:
    memories_path = os.path.join(script_path, "memories")
    current_structure_file = "CurrentFolderStructure.txt"
    print_colored("Memories folder exists. Checking folder structure...", "blue")
    current_folder_structure = get_current_folder_structure(memories_path)

    # Create CurrentFolderStructure.txt if it doesn't exist
    if not os.path.exists(os.path.join(memories_path, current_structure_file)):
        print_colored("CurrentFolderStructure.txt not found. Creating it...", "blue")
        with open(os.path.join(memories_path, current_structure_file), "w") as f:
            f.write("\n".join(current_folder_structure))

    with open(os.path.join(memories_path, current_structure_file), "r") as f:
        original_folder_structure = f.read().splitlines()
    structures_match = compare_folder_structures(original_folder_structure, current_folder_structure)
    if not structures_match:
        print_colored("Folder structures differ. Re-initializing memory mapping...", "yellow")
        print_colored("Updating CurrentFolderStructure.txt...", "blue")
        with open(os.path.join(memories_path, current_structure_file), "w") as f:
            f.write("\n".join(current_folder_structure))
        print_colored("Recreating connection map...", "blue")
        folder_list = [(name, os.path.join(memories_path, name)) for name in current_folder_structure]
        find_similar_folders(folder_list)
    else:
        print_colored("Folder structures match. Memory mapping is synchronized.", "green")

def summarize_memory_folder_structure(folder_path, file_path="directory_structure.txt", include_files=True):
    ignore_files = [".\\directory_structure.txt", ".\\Memory_connecions_map.txt"]
    with open(file_path, 'w') as f:
        f.write(f"Directory structure for: {folder_path}\n\n")
        for root, dirs, files in os.walk(folder_path):
            f.write(f"{root}\n")
            if include_files:
                for file in files:
                    full_path = os.path.join(root, file)
                    if full_path not in ignore_files:
                        f.write(f"{full_path}\n")

def get_current_folder_structure(folder_path):
    return [name for name in os.listdir(folder_path) if os.path.isdir(os.path.join(folder_path, name))]

def compare_folder_structures(original, current):
    return set(original) == set(current)
if __name__ == "__main__":
    memories_path = os.path.join(os.path.abspath(os.path.dirname(__file__)), "memories")
    current_structure_file = "CurrentFolderStructure.txt"

    if not os.path.exists(memories_path):
        print_colored("Memories folder does not exist. Proceeding with full initialization...", "yellow")
        print_colored("Creating standard folder structure from template...", "blue")
        create_file_structure(memory_templates)
        print_colored("Creating memory mapping...", "blue")
        folder_list = [(name, os.path.join(memories_path, name)) for name in get_current_folder_structure(memories_path)]
        find_similar_folders(folder_list)

        # Create CurrentFolderStructure.txt
        print_colored("Creating CurrentFolderStructure.txt...", "blue")
        with open(os.path.join(memories_path, current_structure_file), "w") as f:
            f.write("\n".join(get_current_folder_structure(memories_path)))

    else:
        print_colored("Memories folder exists. Checking folder structure...", "blue")
        current_folder_structure = get_current_folder_structure(memories_path)

        # Create CurrentFolderStructure.txt if it doesn't exist
        if not os.path.exists(os.path.join(memories_path, current_structure_file)):
            print_colored("CurrentFolderStructure.txt not found. Creating it...", "blue")
            with open(os.path.join(memories_path, current_structure_file), "w") as f:
                f.write("\n".join(current_folder_structure))

        # Load CurrentFolderStructure.txt
        with open(os.path.join(memories_path, current_structure_file), "r") as f:
            original_folder_structure = f.read().splitlines()

        # Compare folder structures
        structures_match = compare_folder_structures(original_folder_structure, current_folder_structure)
        if not structures_match:
            print_colored("Folder structures differ. Re-initializing memory mapping...", "yellow")
            print_colored("Updating CurrentFolderStructure.txt...", "blue")
            with open(os.path.join(memories_path, current_structure_file), "w") as f:
                f.write("\n".join(current_folder_structure))
            print_colored("Recreating connection map...", "blue")
            folder_list = [(name, os.path.join(memories_path, name)) for name in current_folder_structure]
            find_similar_folders(folder_list)
        else:
            print_colored("Folder structures match. Memory mapping is synchronized.", "green")
    print_colored("Memory initialization complete. System synchronized.", "green")