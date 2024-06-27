#update_focus.py
tool_type_for_Tool_Manager="reflection"




from SelAwareAI_Gemini.PROJECT12.FOCUS import  FocusType, MoscowCategory


def update_focus(focus_manager, focus_name: str, focus_type: str, moscow_category: str, importance: float,
                 difficulty: float, reward: float, total_work: float, proposed_action: str,
                 cost_per_run: float):
  try:
    focus_type_enum = FocusType[focus_type.upper()]
    moscow_category_enum = MoscowCategory[moscow_category.upper()]
  except KeyError as e:
    return f"Invalid enum value: {str(e)}"

  if focus_name in focus_manager.focus_tree:
    return f"Focus point '{focus_name}' already exists. Use update methods to modify existing points."

  focus_manager.add_focus_point(focus_name, focus_type_enum, moscow_category_enum,
                                importance, difficulty, reward, total_work, proposed_action, cost_per_run)
  return f"Focus point '{focus_name}' added successfully."


update_focus_description_json = {
  "function_declarations": [
    {
      "name": "update_focus",
      "description": "Updates or adds a new focus point to the FocusManager. Required: focus_name, focus_type, moscow_category, importance, difficulty, reward, total_work, proposed_action, cost_per_run.",
      "parameters": {
        "type_": "OBJECT",
        "properties": {
          "focus_name": {
            "type_": "STRING",
            "description": "Name of the focus point"
          },
          "focus_type": {
            "type_": "STRING",
            "description": "Type of the focus point"
          },
          "moscow_category": {
            "type_": "STRING",
            "description": "Moscow category of the focus point"
          },
          "importance": {
            "type_": "NUMBER",
            "description": "Importance of the focus point"
          },
          "difficulty": {
            "type_": "NUMBER",
            "description": "Difficulty of the focus point"
          },
          "reward": {
            "type_": "NUMBER",
            "description": "Reward of the focus point"
          },
          "total_work": {
            "type_": "NUMBER",
            "description": "Total work of the focus point"
          },
          "proposed_action": {
            "type_": "STRING",
            "description": "Proposed action for the focus point"
          },
          "cost_per_run": {
            "type_": "NUMBER",
            "description": "Cost per run of the focus point"
          }
        }
      }
    }
  ]
}

update_focus_description_short_str = "Updates or adds a new focus point to the FocusManager"