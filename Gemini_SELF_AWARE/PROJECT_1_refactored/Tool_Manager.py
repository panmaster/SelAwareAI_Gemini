import os
import importlib.util
import google.generativeai as genai
from termcolor import colored, cprint  # Import termcolor for colored printing
import json
from typing import Dict, Tuple

class ToolManager:
    def __init__(self, tools_directory="tools"):
        """Initializes the tool manager by loading tools from the specified directory."""
        print(f"Initializing ToolManager with tools directory: {tools_directory}")
        self.tools_directory = tools_directory
        self.tool_mapping = {}  # Map tool names to functions
        self.all_tools = []  # List of loaded tool descriptions (JSON)
        self.short_descriptions = {}  # Dictionary for short descriptions
        self.categories = {}  # Dictionary to store category information
        self._load_tools()  # Load tools upon initialization

    def _load_tools(self):
        """Scans the tools directory, loads tools, and populates tool_mapping."""
        print(f"Scanning tools directory: {self.tools_directory}")

        for category in os.listdir(self.tools_directory):
            print(f"Found category: {category}")
            category_path = os.path.join(self.tools_directory, category)
            if os.path.isdir(category_path):
                print(f"Entering category directory: {category_path}")
                self.categories[category] = {"tools": []}  # Store the category information

                for filename in os.listdir(category_path):
                    if filename.endswith(".py") and not filename.startswith("_"):
                        print(f"Found Python file: {filename}")
                        tool_name = filename[:-3]  # Remove '.py' extension
                        self._load_tool(category, tool_name)
                        self.categories[category]["tools"].append(tool_name)

    def _load_tool(self, category, tool_name):
        """Loads a single tool from a given category."""
        print(f"Loading tool: {tool_name} from category: {category}")
        module_name = f"{category}.{tool_name}"
        module_path = os.path.join(self.tools_directory, category, f"{tool_name}.py")

        spec = importlib.util.spec_from_file_location(module_name, module_path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)

        # Assume tool function has the same name as the module
        tool_function = getattr(module, tool_name)

        # Get description (assuming naming convention like 'tool_name_description_json')
        description_name = f"{tool_name}_description_json"
        tool_description = getattr(module, description_name, None)

        # Get short description (assuming naming convention like 'tool_name_description_short_str')
        short_description_name = f"{tool_name}_description_short_str"
        short_description = getattr(module, short_description_name, None)

        # Check if the tool exists
        if tool_function is not None:
            print(f"Tool function '{tool_name}' loaded successfully")
            self.tool_mapping[tool_name] = tool_function
            self.all_tools.append(tool_description)
            self.short_descriptions[tool_name] = short_description
            print(f"Tool description: {tool_description}")
            print(f"Short description: {short_description}")
        else:
            print(f"Warning: Could not load tool function '{tool_name}' from '{module_path}'")

    def get_tools_list_json(self):
        """Returns a list of JSON tool descriptions."""
        return self.all_tools

    def get_tools_structure(self):
        """Returns a dictionary representing the structure of the tools folder, including categories."""
        return {
            "categories": self.categories,
            "all_tools": self.all_tools,
            "tool_mapping": self.tool_mapping,
            "short_descriptions": self.short_descriptions
        }

    def print_tools_structure(self):
        """Prints the structure of the tools folder in a colorful and organized way."""

        tools_structure = self.get_tools_structure()

        cprint("\n\n========================================", "magenta")
        cprint("  Tool Manager Structure", "cyan", attrs=["bold"])
        cprint("========================================", "magenta")

        cprint("\nCategories:", "green", attrs=["bold"])
        for category, info in tools_structure["categories"].items():
            cprint(f"  {category}:", "blue", attrs=["bold"])
            for tool_name in info["tools"]:
                cprint(f"    - {tool_name}", "cyan")

        cprint("\n\nTool Descriptions (JSON):", "green", attrs=["bold"])
        for i, tool_json in enumerate(tools_structure["all_tools"]):
            cprint(f"  {i+1}. {tool_json}", "yellow")

        cprint("\n\nTool Mapping:", "green", attrs=["bold"])
        for tool_name, tool_function in tools_structure["tool_mapping"].items():
            cprint(f"  {tool_name}: {tool_function}", "yellow")

        cprint("\n\nShort Tool Descriptions:", "green", attrs=["bold"])
        for tool_name, short_description in tools_structure["short_descriptions"].items():
            cprint(f"  {tool_name}: {short_description}", "cyan")

        cprint("\n\n========================================", "magenta")

        return tools_structure

def ChooseToolByAI(user_prompt: str, tools_structure: Dict) -> str:
    """
    Analyzes the user's prompt using AI and chooses a tool based on keywords,
    ensuring the selected tool returns JSON descriptions.
    """
    for tool_name, tool_description in tools_structure["short_descriptions"].items():
        # Check if the tool returns JSON descriptions
        tool_json = next(item for item in tools_structure["all_tools"] if item["name"] == tool_name)
        if tool_json["return_type"] == "json":
            if any(keyword in user_prompt.lower() for keyword in tool_description.lower().split()):
                return f"Call tool: {tool_name}"
    return "Call tool: none"

def extract_tool_and_arguments_from_ai_response(ai_response: str) -> Tuple[str, str]:
    """
    Extracts the tool name and arguments from the AI's response.
    """
    for line in ai_response.split("\n"):
        if line.startswith("Call tool: "):
            parts = line.split("Call tool: ")
            tool_name = parts[1].strip()
            arguments = parts[1] if len(parts) > 1 else ""
            return tool_name, arguments
    return None, None

def execute_selected_tool(tool_manager: ToolManager, tool_name: str, arguments: str = None) -> str:
    """
    Executes the selected tool and returns the result.
    """
    tool_function = tool_manager.tool_mapping.get(tool_name)
    if tool_function:
        try:
            result = tool_function(arguments)
            print(f"Tool '{tool_name}' executed successfully with result: {result}")
            return result
        except Exception as e:
            print(f"Error executing tool '{tool_name}': {e}")
    else:
        print(f"Tool '{tool_name}' not found.")
    return "Error: Tool not found or execution failed."

class AiToolSelector:
    def __init__(self, tool_manager: ToolManager):
        self.tool_manager = tool_manager
        self.model = self._initialize_model()

    def _initialize_model(self):
        """Initializes the generative AI model with the ToolSelector function."""
        tools_structure = self.tool_manager.get_tools_structure()
        tools = {
            "ToolSelector": {
                "description": "This tool analyzes user input and selects another tool from the available options, ensuring the selected tool returns JSON descriptions.",
                "function": ChooseToolByAI,
            }
        }

        model = genai.GenerativeModel(
            system_instruction="""You are a helpful AI assistant with access to a variety of tools.
            When you need to use a tool, state your request clearly in the following format:
            "Call tool: <tool_name>"

            For example, if you need to list files in a directory, you would say:
            "Call tool: list_files"

            Make sure to provide any necessary arguments or information for the tool.
            """,
            model_name='gemini-1.5-flash-latest',
            safety_settings={'HARASSMENT': 'block_none'},
            tools=tools
        )
        return model

    def select_and_run_tool_from_ai(self, user_prompt: str) -> str:
        """
        Orchestrates the process of selecting and executing a tool using AI.
        """
        ai_response = self.model.start_chat(history=[]).send_message(user_prompt).text
        print(f"AI Response: {ai_response}")
        return self.execute_tool_from_ai_response(ai_response)

    def execute_tool_from_ai_response(self, ai_response: str) -> str:
        """
        Interprets the AI's response, extracts tool information, and executes the tool.
        """
        tool_name, arguments = extract_tool_and_arguments_from_ai_response(ai_response)
        if tool_name:
            return execute_selected_tool(self.tool_manager, tool_name, arguments)
        else:
            return "Error: No tool selected."