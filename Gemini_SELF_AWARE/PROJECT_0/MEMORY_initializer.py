import os
from collections import defaultdict
from fuzzywuzzy import fuzz
from datetime import datetime
import sys
import  json
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


def create_folders_from_structure(structure, base_folder):
    """Recursively creates folders based on the given structure."""
    for key, value in structure.items():
        folder_path = os.path.join(base_folder, key)
        os.makedirs(folder_path, exist_ok=True)
        if isinstance(value, dict):
            create_folders_from_structure(value, folder_path)


def find_similar_folders(folder_list):
    """Finds and returns a dictionary of similar folders."""
    print_colored("Finding similar folders...", "blue")
    similar_folders = defaultdict(list)
    total_combinations = len(folder_list) * (len(folder_list) - 1) // 2  # Total unique combinations
    completed_comparisons = 0  # Track comparisons made

    print_colored(f"  - Total folder combinations: {total_combinations}", "blue")

    # Stage 1: Partial Token Sort Ratio
    print_colored("    - Stage 1: Partial Token Sort Ratio", "blue")
    for i in range(len(folder_list)):
        for j in range(i + 1, len(folder_list)):
            folder_name_1, path_1 = folder_list[i]
            folder_name_2, path_2 = folder_list[j]

            completed_comparisons += 1

            progress_percent = int(completed_comparisons / total_combinations * 100)
            progress_bar = "[" + "#" * progress_percent + "-" * (100 - progress_percent) + "]"
            sys.stdout.write(f"\r      - {progress_bar} {progress_percent}% ")
            sys.stdout.flush()

            similarity_score = fuzz.partial_token_sort_ratio(folder_name_1, folder_name_2)
            similarity_threshold = 80

            if similarity_score >= similarity_threshold:
                similar_folders[folder_name_1].append(path_2)
                similar_folders[folder_name_2].append(path_1)

    # Stage 2: Partial Ratio
    print_colored("    - Stage 2: Partial Ratio", "blue")
    completed_comparisons = 0  # Reset for the second stage
    for i in range(len(folder_list)):
        for j in range(i + 1, len(folder_list)):
            folder_name_1, path_1 = folder_list[i]
            folder_name_2, path_2 = folder_list[j]

            completed_comparisons += 1

            progress_percent = int(completed_comparisons / total_combinations * 100)
            progress_bar = "[" + "#" * progress_percent + "-" * (100 - progress_percent) + "]"
            sys.stdout.write(f"\r      - {progress_bar} {progress_percent}% ")
            sys.stdout.flush()

            similarity_score = fuzz.partial_ratio(folder_name_1, folder_name_2)
            similarity_threshold = 70

            if similarity_score >= similarity_threshold:
                similar_folders[folder_name_1].append(path_2)
                similar_folders[folder_name_2].append(path_1)

    print("")  # Print a newline after the progress bar
    return similar_folders

def create_memory_connections_map(similar_folders, file_path):
    """Creates the Memory_connections_map.txt file."""
    with open(file_path, "w") as f:
        for folder_name, paths in similar_folders.items():
            f.write(f"**** {folder_name} ****\n")
            for path in paths:
                f.write(f"  Path: {path}\n")
            f.write("\n")


def update_current_folder_structure(folder_path, file_path):
    """Updates the CurrentFolderStructure.txt file."""
    current_structure = {}
    for item in os.listdir(folder_path):
        item_path = os.path.join(folder_path, item)
        if os.path.isdir(item_path):
            current_structure[item] = update_current_folder_structure(item_path, None)
        else:
            current_structure[item] = []
    if file_path is not None:  # Only write to file if file_path is provided
        with open(file_path, 'w') as f:
            json.dump(current_structure, f, indent=4)
    return current_structure


def compare_folder_structures(original, current):
    """
    Compares folder structures represented as dictionaries.
    Returns True if the original structure is a subset of the current
    structure (allowing for additional folders in the current structure).
    """
    for key, value in original.items():
        if key not in current:
            return False  # Key from original not found in current
        if isinstance(value, dict) and not compare_folder_structures(value, current[key]):
            return False  # Recursive check failed for nested folders
    return True  # All keys and nested structures from original found in current


def initialize_memories():
    """Initializes the memory folder structure and mappings."""
    script_path = os.path.abspath(os.path.dirname(__file__))
    memories_path = os.path.join(script_path, "memory")
    base_structure_file = os.path.join(memories_path, "BaseFileStructure.txt")
    current_structure_file = os.path.join(memories_path, "CurrentFolderStructure.txt")
    memory_connections_file = os.path.join(memories_path, "Memory_connections_map.txt")

    def get_current_folder_structure(folder_path):
        """Retrieves the current folder structure as a dictionary."""
        return update_current_folder_structure(folder_path, None)

    def get_folder_structure_from_file(file_path):
        """Retrieves folder structure from a file."""
        try:
            with open(file_path, "r") as f:
                structure = json.load(f)
            return structure
        except FileNotFoundError:
            return {}

    # 1. Check if memory folder exists:
    if not os.path.exists(memories_path):
        print_colored("Memories folder does not exist. Proceeding with full initialization...", "yellow")
        os.makedirs(memories_path, exist_ok=True)

        # 2. Create folder structure from templates and populate folder_list:
        folder_list = []
        for template_name, template_data in memory_templates.items():
            template_name_safe = template_name.replace(":", "_")
            template_folder = os.path.join(memories_path, template_name_safe)
            create_folders_from_structure(template_data["structure"], template_folder)

            folder_list.append((template_name_safe, template_folder))
            for root, dirs, _ in os.walk(template_folder):
                for dir_name in dirs:
                    folder_list.append((dir_name, os.path.join(root, dir_name)))

        # 3. Create BaseFileStructure.txt:
        with open(base_structure_file, "w") as f:
            json.dump(get_current_folder_structure(memories_path), f, indent=4)

        # 4. Find similar folders and create the connection map:
        similar_folders = find_similar_folders(folder_list)
        create_memory_connections_map(similar_folders, memory_connections_file)

        # 5. Create/update CurrentFolderStructure.txt:
        update_current_folder_structure(memories_path, current_structure_file)

    else:  # Memories folder exists
        print_colored("Memories folder exists. Checking folder structure...", "blue")

        # 7. Load original folder structure from BaseFileStructure.txt:
        original_folder_structure = get_folder_structure_from_file(base_structure_file)

        # 8. Get the current folder structure:
        current_folder_structure = get_current_folder_structure(memories_path)

        # 9. Compare structures and update if necessary:
        if not compare_folder_structures(original_folder_structure, current_folder_structure):
            print_colored("Base folder structure is not a subset of the current structure. Updating...", "yellow")

            # Update folder structure (add new folders from templates)
            for template_name, template_data in memory_templates.items():
                template_name_safe = template_name.replace(":", "_")
                template_folder = os.path.join(memories_path, template_name_safe)
                create_folders_from_structure(template_data["structure"], template_folder)

            # Update the CurrentFolderStructure.txt to reflect the changes
            update_current_folder_structure(memories_path, current_structure_file)

            # You should also update the Memory_connections_map.txt here.
            # You can either re-run find_similar_folders and create_memory_connections_map
            # or implement logic to smartly update the existing map with new connections.

        else:
            print_colored("Folder structures compatible. Memory mapping is synchronized.", "green")

    print_colored("Memory initialization complete. System synchronized.", "green")


if __name__ == "__main__":
    initialize_memories()