import json
tool_type_for_Tool_Manager = "all"

def SetFocus(current_focus, focus_strength, goal, subgoals, turn, current_cost, frustration_level, short_term_goals,
             long_term_goals, when_to_difocus):

    data = {
        "current_focus": current_focus,
        "focus_strength": focus_strength,
        "goal": goal,
        "subgoals": subgoals,
        "turn": turn,
        "current_cost": current_cost,
        "frustration_level": frustration_level,
        "short_term_goals": short_term_goals,
        "long_term_goals": long_term_goals,
        "when_to_difocus": when_to_difocus
    }

    file_path = "../../Brain_settings.focus.json"
    with open(file_path, "w") as file:
        json.dump(data, file, indent=2)


SetFocus_description_json = {
    'function_declarations': [
        {
            'name': 'SetFocus',
            'description': 'Saves the AI\'s current focus, goals, and related parameters to a JSON file for persistence.',
            'parameters': {
                'type_': 'OBJECT',
                'properties': {
                    'current_focus': {'type_': 'STRING', 'description': 'The AI\'s current area of concentration.'},
                    'focus_strength': {'type_': 'INTEGER',
                                       'description': 'A measure (0.0 to 1.0) of the AI\'s focus level.'},
                    'goal': {'type_': 'STRING', 'description': 'The AI\'s primary objective.'},
                    'subgoals': {'type_': 'ARRAY',
                                 'description': 'A list of smaller goals that contribute to the main goal.'},
                    'turn': {'type_': 'INTEGER',
                             'description': 'The current time step or turn in the AI\'s operation.'},
                    'current_cost': {'type_': 'INTEGER', 'description': 'The accumulated cost or effort spent so far.'},
                    'frustration_level': {'type_': 'INTEGER',
                                          'description': 'A measure (0.0 to 1.0) of the AI\'s frustration.'},
                    'short_term_goals': {'type_': 'ARRAY', 'description': 'A list of short-term goals.'},
                    'long_term_goals': {'type_': 'ARRAY', 'description': 'A list of long-term goals.'},
                    'when_to_difocus': {'type_': 'STRING',
                                        'description': 'The condition or trigger that would cause the AI to shift its focus.'}
                }
            }
        }
    ]
}

SetFocus_description_short_str = "Saves the AI's current focus, goals, and related parameters to a JSON file."