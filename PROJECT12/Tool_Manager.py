import os
import importlib.util
import json
from typing import Dict, List, Callable, Any, Optional
import logging

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class ToolManager:
    def __init__(self, tools_directory="tools"):
        print(f"\033[92mInitializing ToolManager with tools directory: {tools_directory}\033[0m")
        self.tools_directory = tools_directory
        self.tool_mapping: Dict[str, Callable] = {}  # Maps tool names to functions
        self.all_tools: List[Dict] = []  # Stores tool metadata
        self.categories: Dict[str, Dict] = {}  # Stores tools by category
        self.tool_types: Dict[str, str] = {}  # Maps tool names to their types
        self.valid_tool_types = {"all", "input", "reflection", "action", "web","emotions"}
        self._load_tools()
        self.tool_usage: Dict[str, Dict[str, float]] = {}  # Track usage and success metrics

    def record_tool_usage(self, tool_name, success_metric: float = None):
        """Records tool usage and success metrics."""
        self.tool_usage[tool_name] = self.tool_usage.get(tool_name, {"usage": 0, "success": 0})
        self.tool_usage[tool_name]["usage"] += 1
        if success_metric is not None:
            self.tool_usage[tool_name]["success"] += success_metric

    def get_tool_usage_stats(self):
        """Returns the tool usage statistics."""
        return {tool: self.tool_usage.get(tool, 0) for tool in self.tool_mapping}

    def _load_tools(self) -> None:
        """Loads tools from the specified directory."""
        print(f"\033[92mScanning tools directory: {self.tools_directory}\033[0m")
        for category in os.listdir(self.tools_directory):
            category_path = os.path.join(self.tools_directory, category)
            if os.path.isdir(category_path):
                print(f"  \033[94mFound category: {category}\033[0m")
                self.categories[category] = {"tools": []}
                for filename in os.listdir(category_path):
                    if filename.endswith(".py") and not filename.startswith("_"):
                        self._load_tool(category, filename[:-3])

    def _load_tool(self, category: str, tool_name: str) -> None:
        """Loads a single tool from a Python file."""
        try:
            module_name = f"{category}.{tool_name}"
            module_path = os.path.join(self.tools_directory, category, f"{tool_name}.py")
            spec = importlib.util.spec_from_file_location(module_name, module_path)
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)

            tool_function: Callable = getattr(module, tool_name, None)
            description_name = f"{tool_name}_description_json"
            tool_description: dict = getattr(module, description_name, None)
            tool_type: str = getattr(module, "tool_type_for_Tool_Manager", "all")

            if tool_function and tool_description:
                print(f"      \033[92m- Tool function '{tool_name}' loaded successfully\033[0m")
                self.tool_mapping[tool_name] = tool_function
                tool_info = {
                    "name": tool_name,
                    "description": tool_description,
                    "category": category,
                    "type": tool_type
                }
                self.all_tools.append(tool_info)
                self.tool_types[tool_name] = tool_type
                self.categories[category]["tools"].append(tool_name)  # Add the tool to the category
            else:
                print(f"      \033[91m- Warning: Could not load tool function or description for '{tool_name}'\033[0m")

        except Exception as e:
            print(f"      \033[91m- Error loading tool '{tool_name}': {e}\033[0m")

    def get_filtered_tools(self, tool_type: str = "all") -> List[Dict]:
        """Returns a filtered list of tool information dictionaries."""
        if tool_type not in self.valid_tool_types:
            logger.warning(f"Invalid tool type '{tool_type}'. Using 'all' instead.")
            tool_type = "all"

        return [tool for tool in self.all_tools if tool_type == "all" or tool["type"] == tool_type]

    def get_tools_list_json(self, tool_type: str = "all") -> str:
        """Returns a JSON string of tools for a given tool type."""
        filtered_tools = self.get_filtered_tools(tool_type)
        return json.dumps([tool["description"] for tool in filtered_tools], indent=2)

    def get_tools_structure(self) -> Dict:
        """Returns a dictionary representing the structure of loaded tools."""
        return {
            "categories": self.categories,
            "all_tools": self.all_tools,
            "tool_mapping": list(self.tool_mapping.keys()),  # Just the tool names
            "tool_types": self.tool_types
        }

    def print_tools_structure(self):
        """Prints the structure of the loaded tools."""
        tools_structure = self.get_tools_structure()
        print("\n\n\033[95m=========================================\033[0m")
        print(f"  \033[96mTool Manager Structure\033[0m")
        print("\033[95m=========================================\033[0m")
        print(f"\n\033[92mCategories:\033[0m")
        for category, info in tools_structure["categories"].items():
            print(f"  \033[94m- {category}:\033[0m")
            for tool_name in info["tools"]:
                print(f"    \033[96m- {tool_name}\033[0m")
        print(f"\n\n\033[92mTool Descriptions:\033[0m")
        for i, tool in enumerate(tools_structure["all_tools"], 1):
            print(f"  \033[93m{i}. {json.dumps(tool, indent=2)}\033[0m")
        return tools_structure

    def update_tool_priorities(self, priorities: Dict[str, float]):
        """Updates the priorities of tools based on the provided dictionary."""
        for tool_name, priority in priorities.items():
            if tool_name in self.tool_mapping:
                # You might want to store this priority in a separate attribute
                # for later use. For example, self.tool_priorities[tool_name] = priority
                print(f"Updated priority for {tool_name}: {priority}")

    def prioritize_tools(self, reflection_chat: Any) -> None:
        """Prioritizes tools based on usage and success metrics, using a Gemini model."""
        print(f"Prioritizing Tools")
        try:
            tool_usage = self.tool_usage
            weights = {"usage": 0.5, "success": 0.3, "efficiency": 0.2}  # Example weights
            prioritization_prompt = f"""
            Analyze tool usage and suggest prioritization based on the following data:
            {json.dumps(tool_usage, indent=2)} 
            Weights:
            {json.dumps(weights, indent=2)}
            Provide your response as a JSON object with tool names as keys and their priorities as values (0.0 to 1.0).
            """
            prioritization_response = reflection_chat.send_message(prioritization_prompt)

            try:
                tool_priorities: Dict[str, float] = json.loads(prioritization_response.text)
                self.update_tool_priorities(tool_priorities)
            except json.JSONDecodeError as e:
                logger.warning(f"Could not parse tool prioritization response as JSON: {e}")
                logger.info(f"Raw response: {prioritization_response.text}")
        except AttributeError as e:
            logger.warning(f"Error in prioritize_tools: {e}")

    def get_tool_by_name(self, tool_name: str) -> Optional[Callable]:
        """Returns the tool function based on its name."""
        return self.tool_mapping.get(tool_name)

    def get_tools_by_type(self, tool_type: str) -> List[str]:
        """Returns a list of tool names for a specific type."""
        return [tool["name"] for tool in self.all_tools if tool["type"] == tool_type]

    def reload_tools(self) -> None:
        """Reloads all tools from the tools directory."""
        print(f"Reloading tools from {self.tools_directory}...")
        self.tool_mapping = {}
        self.all_tools = []
        self.categories = {}
        self.tool_types = {}
        self._load_tools()
        print("Tools reloaded.")

    def add_tool(self, tool_info: Dict) -> None:
        """Adds a new tool to the tool manager."""
        print(f"Adding tool: {tool_info['name']}...")
        self.all_tools.append(tool_info)
        self.tool_types[tool_info["name"]] = tool_info["type"]
        self.categories[tool_info["category"]]["tools"].append(tool_info["name"])
        self.tool_mapping[tool_info["name"]] = getattr(importlib.import_module(
            f"{tool_info['category']}.{tool_info['name']}"), tool_info["name"])
        print("Tool added successfully.")