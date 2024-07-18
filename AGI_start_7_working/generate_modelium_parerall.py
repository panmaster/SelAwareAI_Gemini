import re
from typing import Dict, Callable, Any, Tuple, List
import json
import logging
import os
import importlib
import asyncio  # For asynchronous operations
import random
import time

# --- Set up logging ---
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


# --- Simulated Asynchronous AI Model ---
async def ai_model(prompt: str, tools: list = None) -> Any:
    """
    Simulates an asynchronous AI model call (replace with your actual AI integration).

    Args:
        prompt: The prompt string for the model.
        tools: A list of tool functions (can be ignored in this simulation).

    Returns:
        A dictionary representing the AI's response.
    """
    logger.info(f"AI Model called with prompt: {prompt}")

    # Simulate processing time (replace with your actual model call)
    await asyncio.sleep(random.uniform(1, 3))  # Simulate 1-3 seconds of thinking

    # Simulated response - adapt based on your AI model's output format
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

    def get_tools_by_type(self, tool_type: str) -> List[Tool]:
        """Returns a list of tools based on their type."""
        return [tool for tool in self.tools.values() if tool.tool_type == tool_type]


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

# --- Hierarchical Modelium Execution (with Parallelism and Async) ---
async def CreateHierarchicalModelium(
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
    generated_code = ""

    for i, (config_key, config) in enumerate(configs.items()):
        if not all(key in config for key in ["model_name", "model_type", "prompt"]):
            raise ModeliumCreationError("Invalid model configuration: missing keys.")

        model_name = config["model_name"]
        logger.info(f"Generating code for model: {model_name} (Level {level})")

        # --- Prompt Construction ---
        generated_code += f"    # --- Model {config_key} ---\n"
        generated_code += f"    prompt_{i} = f'''{config['prompt']}'''\n"

        # Add parent and shared data to the prompt
        if parent_data:
            generated_code += f"    prompt_{i} = prompt_{i}.format(**{parent_data})\n"
        if shared_data:
            generated_code += f"    prompt_{i} = prompt_{i}.format(**{shared_data})\n"

        # --- Parallel Model Execution (Asynchronous) ---
        if "parallel_models" in config:
            generated_code += f"    # --- Parallel Models (Group {i}) ---\n"
            generated_code += f"    parallel_results_{i} = await asyncio.gather(*[\n"

            for j, parallel_config in enumerate(config["parallel_models"]):
                parallel_model_name = parallel_config["model_name"]
                generated_code += f"        run_model(\n"
                generated_code += f"            model_config={json.dumps(parallel_config)},\n"
                generated_code += f"            tool_registry=tool_registry,\n"
                generated_code += f"            parent_data=outputs,\n"
                generated_code += f"            shared_data=shared_data\n"
                generated_code += f"        )"
                if j < len(config["parallel_models"]) - 1:
                    generated_code += ",\n"  # Add a comma for all but the last

            generated_code += f"    ])\n"
            generated_code += f"    outputs['parallel_group_{i}_results'] = parallel_results_{i}\n"
        else:
            # --- Standard Model Execution (Asynchronous) ---
            # Tool Access (adjust logic as needed)
            tools_code = "[]"
            if config.get("tool_access") == "all":
                tools_code = "tool_registry.get_all_tools()"
            elif config.get("tool_access") and '|' in config.get("tool_access"):
                requested_types = config.get("tool_access").split('|')
                tools_code = f"tool_registry.get_tools_by_type('{requested_types[0]}')"  # Use get_tools_by_type
                # ... (add other tool access options if necessary) ...

            # Model Execution (using the placeholder ai_model)
            generated_code += f"    response_{i} = await run_model(model_config={json.dumps(config)}, tool_registry=tool_registry, parent_data=outputs, shared_data=shared_data)\n"
            generated_code += f"    text_{i} = extract_text_from_response(response_{i})\n"
            generated_code += f"    outputs['{config_key}'] = text_{i}\n"
            generated_code += f"    logger.info(f'{config_key} Output: {{text_{i}}}')\n"
            # --- Tool Usage ---
            if config.get("use_interpreter", False) and tool_registry:
                generated_code += f"    tool_results_{i} = interpret_function_calls(text_{i}, tool_registry)\n"
                generated_code += f"    outputs['{config_key}_tool_results'] = tool_results_{i}\n"

        # --- Recursive Call (for Child Models) ---
        if "children" in config and level < max_depth:
            child_outputs, child_code = await CreateHierarchicalModelium(
                config["children"], level + 1, max_depth, tool_registry,
                parent_data=outputs, shared_data=shared_data
            )
            outputs.update(child_outputs)
            generated_code += child_code

    return outputs, generated_code


async def run_model(model_config, tool_registry, parent_data, shared_data):
    """Helper function to execute a single model."""
    model_name = model_config['model_name']
    prompt = model_config['prompt'].format(**parent_data, **shared_data)

    # Tool Access (adjust logic as needed)
    tools = []
    if model_config.get("tool_access") == "all":
        tools = tool_registry.get_all_tools()
    elif model_config.get("tool_access") and '|' in model_config.get("tool_access"):
        requested_types = model_config.get("tool_access").split('|')
        tools = tool_registry.get_tools_by_type(requested_types[0])  # Use get_tools_by_type
        # ... (add other tool access options if necessary) ...

    response = await ai_model(prompt, tools=tools)
    text = extract_text_from_response(response)
    logger.info(f"{model_name} Output: {text}")

    if model_config.get("use_interpreter", False) and tool_registry:
        tool_results = interpret_function_calls(text, tool_registry)
        return text, tool_results
    else:
        return text


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
            "use_interpreter": True,
            "tool_access": "all",
            "parallel_models": [  # Example of parallel models
                {
                    "model_name": "Parallel_Model_1",
                    "model_type": "your_model_type",
                    "prompt": "Parallel Model 1 Prompt: {Model_A} - Shared: {shared_value}",
                    "use_interpreter": False,
                    "tool_access": "weather"
                },
                {
                    "model_name": "Parallel_Model_2",
                    "model_type": "your_model_type",
                    "prompt": "Parallel Model 2 Prompt: {Model_A} - Shared: {shared_value}",
                    "use_interpreter": False,
                    "tool_access": "weather"
                }
            ],
            "children": {
                "Model_B1": {
                    "model_name": "Model_B1",
                    "model_type": "your_model_type",
                    "prompt": "Model B1 Prompt. Parent output: {Model_A}",
                    "use_interpreter": False,
                },
                "Model_B2": {
                    "model_name": "Model_B2",
                    "model_type": "your_model_type",
                    "prompt": "Model B2 Prompt. Parent output: {Model_A}",
                    "use_interpreter": False,
                }
            }
        }
    }
    try:
        # Run the asynchronous Modelium
        modelium_output, generated_code = asyncio.run(
            CreateHierarchicalModelium(
                hierarchical_model_configs,
                tool_registry=tool_registry,
                shared_data={"shared_value": "This is shared!"}
            )
        )
        print("Generated Code:\n", generated_code)
        print(json.dumps(modelium_output, indent=4))
    except ModeliumCreationError as e:
        print(f"Error creating Modelium: {e}")