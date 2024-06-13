import json
from collections import defaultdict

def extract_entries_smart(response_message):
    entries = []

    # Find the start and end of the JSON block
    json_start = response_message.find("```json\n")
    json_end = response_message.find("\n```")

    # If JSON block is found, extract the JSON data
    if json_start != -1 and json_end != -1:
        try:
            json_data = response_message[json_start + 9:json_end]  # Extract JSON string
            response_data = json.loads(json_data)

            # --- Extract data using matching rules ---
            entry = defaultdict(list)
            try:
                # 1. Direct Matching:
                for key, value in response_data.items():
                    # Direct match for single-value fields:
                    if key in ["concise_summary", "main_topic", "problem_solved", "concept_definition",
                               "category", "subcategory", "memory_about", "interaction_type",
                               "positive_impact", "negative_impact", "expectations", "object_states",
                               "short_description", "description", "strength_of_experience",
                               "personal_information", "obtained_knowledge"]:
                        entry[key] = value

                    # Direct match for list-type fields:
                    elif key in ["keywords", "entities", "actions", "facts", "contradictions_paradoxes", "people",
                                 "objects", "animals", "scientific_data", "tags", "tools_and_technologies",
                                 "example_projects", "best_practices", "common_challenges", "debugging_tips",
                                 "related_concepts", "visualizations"]:
                        if isinstance(value, list):  # Ensure 'value' is a list
                            entry[key].extend(value)
                        else:
                            entry[key].append(value)  # Append if it's a single value

                    # Handle list of dictionaries:
                    elif isinstance(value, list) and len(value) > 0 and isinstance(value[0], dict):
                        entry[key].extend(value)

                # 2. Keyword-Based Mapping:
                for key, value in response_data.items():
                    if "keyword" in key.lower() and isinstance(value, list):
                        entry["keywords"].extend(value)
                    elif "description" in key.lower():
                        entry["description"] = value
                    elif "summary" in key.lower():
                        entry["concise_summary"] = value
                    elif "step" in key.lower() and isinstance(value, list) and len(value) > 0 and isinstance(value[0], dict):
                        entry["implementation_steps"].extend(value)  # For Template 2
                    elif "resource" in key.lower() and isinstance(value, list) and len(value) > 0 and isinstance(value[0], dict):
                        entry["resources"].extend(value)  # For Template 2
                    elif "code" in key.lower() and isinstance(value, list) and len(value) > 0 and isinstance(value[0], dict):
                        entry["code_examples"].extend(value)  # For Template 2

                # 3. Additional Matching:
                for key, value in response_data.items():
                    if "interaction_type" in key.lower():
                        entry["interaction_type"].extend(value)
                    if "category" in key.lower():
                        entry["category"] = value
                    if "subcategory" in key.lower():
                        entry["subcategory"] = value

                # Append the entry to the list (formatted with yellow color)
                entries.append(dict(entry))  # Convert back to regular dict

            except Exception as e:
                print(f"Error extracting entry: {e}")

        except json.JSONDecodeError:
            print("Error: Invalid JSON in response message.")

    return entries

def format_dict_with_colors(dictionary):
    """
    Formats a dictionary with colors for better readability.

    Args:
        dictionary: The dictionary to format.

    Returns:
        The formatted dictionary with colored key-value pairs.
    """
    yellow = "\033[33m"
    red = "\033[31m"
    reset = "\033[0m"
    formatted_dict = {}
    for key, value in dictionary.items():
        if isinstance(value, list):
            formatted_dict[f"{yellow}{key}{reset}"] = [f"{yellow}{item}{reset}" for item in value]
        elif isinstance(value, dict):
            formatted_dict[f"{yellow}{key}{reset}"] = format_dict_with_colors(value)
        else:
            formatted_dict[f"{yellow}{key}{reset}"] = f"{yellow}{value}{reset}"
    return formatted_dict
