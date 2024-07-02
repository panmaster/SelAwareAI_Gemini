import google.generativeai as genai
from Tool_Manager import ToolManager
import ast
import  re
import os
from  colors import COLORS
MODEL_NAME = 'gemini-1.5-flash-latest'
import  datetime
# Use environment variable for API key
genai.configure(api_key='AIzaSyA60tGw6fZwQdamW8sm6pkgRh5W559kLJ0')
import  hashlib
import time
import  json
def create_session_with_sanitisation():
    """
    Create a session identifier based on the current date and time, ensuring uniqueness and some basic sanitization.
    """
    # Get the current date and time
    now = datetime.datetime.now()

    # Create a string from the current date and time
    date_time_str = now.strftime("%Y-%m-%d %H:%M:%S.%f")

    # Encode the date_time_str to bytes
    date_time_bytes = date_time_str.encode('utf-8')

    # Create a SHA-256 hash of the date_time_bytes
    hash_object = hashlib.sha256(date_time_bytes)

    # Get the hexadecimal representation of the hash
    session_id = hash_object.hexdigest()

    return session_id






# Create a session with sanitisation
session = create_session_with_sanitisation()

def initialize_awareness_loop_models():
    """Initializes models for each stage of the awareness loop."""

    tool_manager = ToolManager()

    # Introspection Stage
    introspection_instruction = "Assess the system's current state and capabilities."
    introspection_tools = tool_manager.get_tools_list_json(tool_type='action_execution')
    introspection_tools_load = ast.literal_eval(introspection_tools)

    introspection_model = genai.GenerativeModel(
        system_instruction=introspection_instruction,
        model_name=MODEL_NAME,
        tools=introspection_tools_load,
        safety_settings={"HARASSMENT": "block_none"}).start_chat(history=[])

    # Action Planning Stage
    action_planning_instruction = "Based on the system's current state, propose actions to achieve the system's goals. "
    action_planning_tools = tool_manager.get_tools_list_json(tool_type='action_execution')
    action_planning_tools_load = ast.literal_eval(action_planning_tools)

    action_planning_model = genai.GenerativeModel(
        system_instruction=action_planning_instruction,
        model_name=MODEL_NAME,
        tools=action_planning_tools_load,
        safety_settings={"HARASSMENT": "block_none"}).start_chat(history=[])

    # Action Execution Stage
    action_execution_instruction = "Execute the planned actions and report the results. you can call  functions"
    action_execution_tools = tool_manager.get_tools_list_json(tool_type='action_execution')
    action_execution_tools_load = ast.literal_eval(action_execution_tools)
    action_execution_model = genai.GenerativeModel(
        system_instruction=action_execution_instruction,
        model_name=MODEL_NAME,
        tools=action_execution_tools_load,
        safety_settings={"HARASSMENT": "block_none"}).start_chat(history=[])

    # Results Evaluation Stage
    results_evaluation_instruction = "Evaluate the results of the executed actions against the system's goals."
    results_evaluation_tools = tool_manager.get_tools_list_json(tool_type='action_execution')
    results_evaluation_tools_load = ast.literal_eval(results_evaluation_tools)
    results_evaluation_model = genai.GenerativeModel(
        system_instruction=results_evaluation_instruction,
        model_name=MODEL_NAME,
        tools=results_evaluation_tools_load,
        safety_settings={"HARASSMENT": "block_none"}).start_chat(history=[])

    # Knowledge Integration Stage
    knowledge_integration_instruction = "Integrate new insights and learnings into the system's knowledge base."
    knowledge_integration_tools = tool_manager.get_tools_list_json(tool_type='action_execution')
    knowledge_integration_tools_load = ast.literal_eval(knowledge_integration_tools)
    knowledge_integration_model = genai.GenerativeModel(
        system_instruction=knowledge_integration_instruction,
        model_name=MODEL_NAME,
        tools=knowledge_integration_tools_load,
        safety_settings={"HARASSMENT": "block_none"}).start_chat(history=[])

    return (
        introspection_model,
        action_planning_model,
        action_execution_model,
        results_evaluation_model,
        knowledge_integration_model
    )


def extract_text_and_function_call(response):
    """
    Extracts text and function calls from different response schemas,
    including GenerateContentResponse objects. Prints the results.

    Args:
        response: The response object from the API.

    Returns:
        A tuple containing:
            - extracted_text: A string containing all the extracted text.
            - function_calls: A list of dictionaries, where each dictionary represents
              a function call with 'name' and 'args' keys.
    """
    extracted_text = ""
    function_calls = []

    def process_content(content):
        nonlocal extracted_text, function_calls
        if isinstance(content, dict):
            if 'text' in content:
                extracted_text += content['text']
            elif 'function_call' in content:
                function_calls.append({
                    'name': content['function_call'].get('name'),
                    'args': content['function_call'].get('args', {})
                })
        elif isinstance(content, str):
            extracted_text += content

    # Handle GenerateContentResponse object
    if hasattr(response, 'result'):
        response = response.result

    # Handle different response schemas
    if isinstance(response, dict):
        if 'candidates' in response:
            for candidate in response['candidates']:
                if 'content' in candidate:
                    content = candidate['content']
                    if 'parts' in content:
                        for part in content['parts']:
                            process_content(part)
                    else:
                        process_content(content)
        else:
            process_content(response)
    elif isinstance(response, str):
        extracted_text = response

    # Print results
    print("Extracted Text:", extracted_text.strip())
    print("Function Calls:", function_calls)

    return extracted_text.strip(), function_calls


# Example usage:


def awareness_loop():
    """Main loop for the awareness loop."""

    introspection_model, action_planning_model, action_execution_model, results_evaluation_model, knowledge_integration_model = initialize_awareness_loop_models()
    counter = 0
    previous_feedback = ""
    userInput=""
    while True:
        try:
            if counter % 3 == 0:
                userInput = input("admin input:")
            print(f"Awareness Loop {counter}")

            # 1. Introspection
            time.sleep(0.2)
            introspection_prompt = f"{counter}Previous loop feedback: {previous_feedback}\n  All inputs, self introspection, you can use  funcion calls"
            introspection_prompt += userInput
            introspection_response = introspection_model.send_message(introspection_prompt)

            print(f"{COLORS['light_green']}INTROSPECTION ")
            print(introspection_response)
            text, function = extract_text_and_function_call(introspection_response.text)


            # 2. Action Planning
            time.sleep(0.2)
            if introspection_response.text is not None:
                 action_planning_prompt = introspection_response.text
            action_planning_prompt += "\nBased on this introspection, develop a strategic plan of actions. Consider short-term and long-term goals, potential obstacles, and available resources."
            action_planning_response = action_planning_model.send_message(action_planning_prompt)
            print(f"{COLORS['light_blue']}ACTION PLANNING ")
            print( action_planning_response)
            text, function = extract_text_and_function_call(action_planning_response.text)


            # 3. Action Execution
            time.sleep(0.2)
            if introspection_response.text is not None:
                 action_execution_prompt = action_planning_response.text
            action_execution_prompt += "\nExecute the planned actions. Provide a detailed report on the steps taken, any challenges encountered, and immediate outcomes."
            action_execution_response = action_execution_model.send_message(action_execution_prompt)
            print(  action_execution_response)
            print(f"{COLORS['light_cyan']}ACTION EXECUTION ")
            text, function = extract_text_and_function_call(action_execution_response.text)


            # 4. Results Evaluation
            time.sleep(0.2)
            if introspection_response.text is not None:
                results_evaluation_prompt = action_execution_response.text
            results_evaluation_prompt += "\nCritically evaluate the results of the executed actions. Assess their effectiveness, identify any unexpected outcomes, and determine the degree of goal achievement."
            results_evaluation_response = results_evaluation_model.send_message(results_evaluation_prompt)
            print(f"{COLORS['light_magenta']}RESULTS EVALUATION ")
            print(results_evaluation_response)
            text, function = extract_text_and_function_call(results_evaluation_response.text)


            # 5. Knowledge Integration
            time.sleep(0.2)
            if introspection_response.text is not None:
                knowledge_integration_prompt = results_evaluation_response.text
            knowledge_integration_prompt += "\nIntegrate the new insights and learnings from this iteration into the system's knowledge base. Identify key takeaways, update existing knowledge, and suggest areas for future focus or improvement."
            knowledge_integration_response = knowledge_integration_model.send_message(knowledge_integration_prompt)
            print(f"{COLORS['light_yellow']}KNOWLEDGE INTEGRATION ")
            print(knowledge_integration_response)
            text, function = extract_text_and_function_call(knowledge_integration_response.text)


            # Update for next iteration
            previous_feedback = knowledge_integration_response.text
            counter += 1

            filepath= "log_"+ str(session)
            print("saving log")
            with open(filepath, "a+") as f:
                f.write(f"----------------------Loop {counter}---------------------------")
                f.write(f"INTROSPECTION PROMPT:\n{introspection_prompt}\n")
                f.write(f"INTROSPECTION RESPONSE:\n{introspection_response}\n****\n")
                f.write(f"ACTION PLANNING PROMPT:\n{action_planning_prompt}\n")
                f.write(f"ACTION PLANNING RESPONSE:\n{action_planning_response}\n****\n")
                f.write(f"ACTION EXECUTION PROMPT:\n{action_execution_prompt}\n")
                f.write(f"ACTION EXECUTION RESPONSE:\n{action_execution_response}\n****\n")
                f.write(f"RESULTS EVALUATION PROMPT:\n{results_evaluation_prompt}\n")
                f.write(f"RESULTS EVALUATION RESPONSE:\n{results_evaluation_response}\n****\n")
                f.write(f"KNOWLEDGE INTEGRATION PROMPT:\n{knowledge_integration_prompt}\n")
                f.write(f"KNOWLEDGE INTEGRATION RESPONSE:\n{knowledge_integration_response}\n****\n")


        except Exception as e:
            print(f"{COLORS['red']}Error occurred: {e} ")


if __name__ == "__main__":
    awareness_loop()