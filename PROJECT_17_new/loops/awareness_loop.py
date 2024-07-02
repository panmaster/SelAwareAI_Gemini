import google.generativeai as genai
from ..managment.Tool_Manager import  ToolManager
from  ..colors import  COLORS as COLORS

MODEL_NAME = 'gemini-1.5-flash-latest'

def initialize_awareness_loop_models():
    """Initializes models for each stage of the awareness loop."""

    # Introspection Stage
    introspection_instruction = "Assess the system's current state and capabilities."
    introspection_tools = ToolManager.tool_manager.get_tools_list_json(
        tool_type='introspection')
    introspection_model = genai.GenerativeModel(
        system_instruction=introspection_instruction,
        model_name=MODEL_NAME,
        tools=introspection_tools,
        safety_settings={"HARASSMENT": "block_none"}
    ).start_chat(history=[])

    # Action Planning Stage
    action_planning_instruction = "Based on the system's current state, propose actions to achieve the system's goals."
    action_planning_tools = ToolManager.tool_manager.get_tools_list_json(
        tool_type='action_planning')
    action_planning_model = genai.GenerativeModel(
        system_instruction=action_planning_instruction,
        model_name=MODEL_NAME,
        tools=action_planning_tools,
        safety_settings={"HARASSMENT": "block_none"}
    ).start_chat(history=[])

    # Action Execution Stage (This is a placeholder, you'll need to implement the actual execution)
    action_execution_model = None

    # Results Evaluation Stage
    results_evaluation_instruction = "Evaluate the results of the executed actions against the system's goals."
    results_evaluation_tools = ToolManager.tool_manager.get_tools_list_json(
        tool_type='results_evaluation')
    results_evaluation_model = genai.GenerativeModel(
        system_instruction=results_evaluation_instruction,
        model_name=MODEL_NAME,
        tools=results_evaluation_tools,
        safety_settings={"HARASSMENT": "block_none"}
    ).start_chat(history=[])

    return (
        introspection_model,
        action_planning_model,
        action_execution_model,
        results_evaluation_model
    )

def awareness_loop():
    """Main loop for the awareness loop."""

    introspection_model, action_planning_model, action_execution_model, all_results_evaluation_model = initialize_awareness_loop_models()
    initial_prompt = "Describe the system's current state and capabilities."  # Example initial prompt


    while True:
        # 1. Introspection


        response_introspection = introspection_model.send_message(initial_prompt)
        print("Introspection:", response_introspection)

        # 2. Action Planning
        response_action_planning = action_planning_model.send_message(response_introspection)
        print("Action Planning:", response_action_planning)


        # 3. Action Execution
        response_action = action_execution_model.send_message(response_action_planning)
        print(response_action)




        # 4. Results Evaluation
        response_all_results_evaluation = all_results_evaluation_model.send_message( response_action)
        print("Results Evaluation:",  response_all_results_evaluation)

