import re
from typing import Dict, Callable, Any, Tuple, List
import json
import logging
import os
import importlib

# --- Set up logging ---
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# --- Placeholder for AI Model ---
# Replace with your ACTUAL AI library and model initialization (e.g., Google Gemini)
def ai_model(prompt: str, tools: list = None) -> Any:
    """
    This is a placeholder for your AI model execution logic.
    Replace it with the code that calls your actual AI model.

    Args:
        prompt: The formatted prompt string to send to the AI model.
        tools: (Optional) A list of tools to make available to the model.

    Returns:
        The AI model's response (format depends on your AI library).
    """
    logger.info(f"AI Model called with prompt: {prompt}")
    # Example using a dummy response (REPLACE THIS):
    return {"candidates": [{"content": {"parts": [{"text": f"AI Response to: {prompt}"}]}}]}


class ModeliumCreationError(Exception):
    """Custom exception for Modelium creation errors."""
    pass

# --- Tool Class (from your TOOL_MANAGER.py) ---
class Tool:
    def __init__(self, name: str, function: Callable, description: str,
                 arguments: Dict[str, str], tool_type: str):
        self.name = name
        self.function = function
        self.description = description
        self.arguments = arguments
        self.tool_type = tool_type

    def __repr__(self):
        return (f"Tool(name='{self.name}', function={self.function.__name__}, "
                f"description='{self.description}', arguments={self.arguments}, "
                f"tool_type='{self.tool_type}')")


# --- Tool Registry (Simplified - adapt as needed) ---
class ToolRegistry:
    def __init__(self):
        self.tools = {}

    def register_tool(self, tool: Tool):
        self.tools[tool.name] = tool

    def get_tool(self, name: str) -> Tool:
        return self.tools.get(name)

    def get_all_tools(self) -> List[Tool]:
        return list(self.tools.values())

    def retrieve_tools_by_names(self, tool_names: List[str]) -> List[Callable]:
        """Retrieves tools by their names from the registry."""
        loaded_tools = []
        for tool_name in tool_names:
            tool = self.get_tool(tool_name)
            if tool:
                loaded_tools.append(tool.function)
            else:
                logger.warning(f"Tool '{tool_name}' not found in registry.")
        return loaded_tools


tool_registry = ToolRegistry()

# --- Tool Definitions ---
def register_tools(tool_registry: ToolRegistry) -> None:
    """Registers example tools."""

    def get_current_weather(city: str, country: str) -> str:
        """Fetches weather data (placeholder - replace with API call)."""
        return f"The weather in {city}, {country} is currently pleasant."

    tool_registry.register_tool(
        Tool(
            name="get_current_weather",
            function=get_current_weather,
            description="Gets the current weather for a given city and country.",
            arguments={"city": "The city name.", "country": "The country name."},
            tool_type="weather"
        )
    )
    # Register more tools here...

# --- Response Processing ---
def extract_text_from_response(response: Any) -> str:
    """Extracts text from the AI model's response."""
    extracted_text = ""
    for candidate in response.get('candidates', []):
        for part in candidate.get('content', {}).get('parts', []):
            extracted_text += part.get('text', '')
    return extracted_text.strip()

def interpret_function_calls(response_text: str, tool_registry: ToolRegistry) -> List[Any]:
    """Interprets and executes tool calls from the model's output."""
    tool_call_pattern = r"Tool Name:\s*(.*?)\nArguments:\s*{(.*?)}\n"
    matches = re.findall(tool_call_pattern, response_text, re.DOTALL)
    results = []
    for match in matches:
        tool_name = match[0].strip()
        tool_args_str = match[1].strip()
        try:
            tool_args = json.loads(tool_args_str)
            tool = tool_registry.get_tool(tool_name)
            if tool:
                result = tool.function(**tool_args)
                results.append(result)
                logger.info(f"Tool '{tool_name}' executed with result: {result}")
            else:
                logger.warning(f"Error: Tool '{tool_name}' not found.")
                results.append(f"Error: Tool '{tool_name}' not found.")
        except Exception as e:
            logger.error(f"Error parsing tool arguments or executing tool '{tool_name}': {e}")
            results.append(f"Error executing tool '{tool_name}': {e}")
    return results

# --- Hierarchical Modelium Execution (with Code Generation) ---
def CreateHierarchicalModelium(
        configs: Dict,
        level: int = 1,
        max_depth: int = 3,
        tool_registry: ToolRegistry = None,
        parent_data: Dict = None,
        shared_data: Dict = None
) -> Tuple[Dict, str]:

    if shared_data is None:
        shared_data = {}

    outputs = {}
    generated_code = ""  # Store generated Python code

    for i, (config_key, config) in enumerate(configs.items()):
        if not all(key in config for key in ["model_name", "model_type", "prompt"]):
            raise ModeliumCreationError("Invalid model configuration: missing keys.")

        model_name = config["model_name"]
        logger.info(f"Generating code for model: {model_name} (Level {level})")

        # --- Dynamic Code Generation ---
        generated_code += f"    # --- Model {model_name} ---\n"
        generated_code += f"    prompt_{i} = f'''{config['prompt']}'''\n"

        # Add parent and shared data to the prompt
        if parent_data:
            generated_code += f"    prompt_{i} = prompt_{i}.format(**{parent_data})\n"
        if shared_data:
            generated_code += f"    prompt_{i} = prompt_{i}.format(**{shared_data})\n"

        # Tool Access
        tools_code = "[]"
        if config.get("tool_access") == "all":
            tools_code = "tool_registry.get_all_tools()"
        elif config.get("tool_access") == "tool_chooser":
            tools_code = "[tool_registry.retrieve_tools_by_names]"

        # Model Execution (using the placeholder ai_model)
        generated_code += f"    response_{i} = ai_model(prompt_{i}, tools={tools_code})\n"
        generated_code += f"    text_{i} = extract_text_from_response(response_{i})\n"
        generated_code += f"    outputs['{model_name}'] = text_{i}\n"
        generated_code += f"    logger.info(f'{model_name} Output: {{text_{i}}}')\n"

        # Tool Usage
        if config.get("use_interpreter", False) and tool_registry:
            generated_code += f"    tool_results_{i} = interpret_function_calls(text_{i}, tool_registry)\n"
            generated_code += f"    outputs['{model_name}_tool_results'] = tool_results_{i}\n"

        # Recursive Call (for child models)
        if "children" in config and level < max_depth:
            child_outputs, child_code = CreateHierarchicalModelium(
                config["children"], level + 1, max_depth, tool_registry,
                parent_data=outputs, shared_data=shared_data
            )
            outputs.update(child_outputs)
            generated_code += child_code

    return outputs, generated_code

# --- Example Usage ---
if __name__ == "__main__":
    # Register tools with the ToolRegistry
    register_tools(tool_registry)

    # Define your hierarchical model configuration
    hierarchical_model_configs = {
        "Model_A": {
            "model_name": "Model_A",
            "model_type": "your_model_type",
            "prompt": "Model A Prompt. Shared data: {shared_value}",
            "use_interpreter": True,  # Enable tool use for this model
            "tool_access": "all",
            "children": {
                "Model_B1": {
                    "model_name": "Model_B1",
                    "model_type": "your_model_type",
                    "prompt": "Model B1 Prompt. Parent output: {Model_A}",
                    "use_interpreter": False,
                    "tool_access": "none",  # No tools for this model
                },
                "Model_B2": {
                    "model_name": "Model_B2",
                    "model_type": "your_model_type",
                    "prompt": "Model B2 Prompt. Parent output: {Model_A}",
                    "use_interpreter": False,
                    "tool_access": "none",  # No tools for this model
                }
            }
        }
    }
    try:
        modelium_output, generated_code = CreateHierarchicalModelium(
            hierarchical_model_configs,
            tool_registry=tool_registry,
            shared_data={"shared_value": "This is shared!"}
        )
        print("Generated Code:\n", generated_code)
        # (You can execute 'generated_code' here or save it to a file)
        print(json.dumps(modelium_output, indent=4))

    except ModeliumCreationError as e:
        print(f"Error creating Modelium: {e}")