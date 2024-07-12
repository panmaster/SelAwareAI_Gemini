import importlib
import os
from typing import Dict, List

class Tool:
    """Represents a tool with information about its type and short description (optional)."""
    def __init__(self, name: str, func: callable, tool_type: str = None, short_description: str = None):
        self.name = name
        self.func = func
        self.tool_type = tool_type
        self.short_description = short_description  # Allow for None

    def __str__(self):
        description_str = f"Description: {self.short_description}" if self.short_description else "Description: Unknown"
        return f"Tool: {self.name}\nType: {self.tool_type}\n{description_str}"

class ToolManager:
    """Manages tools, loading them from a directory and providing methods for filtering and accessing them."""
    def __init__(self, tools_path: str):
        self.tools_path = tools_path
        self.tools: Dict[str, Tool] = self._load_tools(self.tools_path)
        self._print_available_tools()  # Print tool information on instantiation

    def _load_tools(self, directory: str) -> Dict[str, Tool]:
        """Loads tools from the specified directory and its subdirectories."""
        tools = {}
        for root, _, files in os.walk(directory):
            for filename in files:
                if filename.endswith(".py") and filename != "__init__.py":
                    module_name = filename[:-3]
                    module_path = os.path.join(root, filename)
                    spec = importlib.util.spec_from_file_location(module_name, module_path)
                    module = importlib.util.module_from_spec(spec)
                    spec.loader.exec_module(module)
                    for name, obj in module.__dict__.items():
                        if callable(obj) and not name.startswith("_"):
                            # Get type (optional) - Using module.__dict__ to access attributes
                            tool_type = module.__dict__.get("tool_type_for_TOOL_MANAGER", None)

                            # Get description (optional)
                            short_description = None
                            for attr_name in module.__dict__:
                                if attr_name.startswith(name) and attr_name.endswith("_short_description"):
                                    short_description = getattr(module, attr_name)
                                    break

                            tools[name] = Tool(name, obj, tool_type, short_description)
        return tools

    def get_tools_by_type(self, tool_type: str) -> List[Tool]:
        """Returns a list of tools of the specified type."""
        return [tool for tool in self.tools.values() if tool.tool_type == tool_type]

    def get_tools_by_description(self, description: str) -> List[Tool]:
        """Returns a list of tools whose short description contains the specified string."""
        return [tool for tool in self.tools.values()
                if tool.short_description and description.lower() in tool.short_description.lower()]

    def get_tool(self, name: str) -> Tool:
        """Returns the tool with the specified name."""
        return self.tools.get(name)

    def _print_available_tools(self):
        """Prints information about all available tools."""
        print("Available tools:")
        for tool in self.tools.values():
            print(tool)
        print("-" * 20)  # Separator

        # Print tools categorized by type
        tool_types = set(tool.tool_type for tool in self.tools.values() if tool.tool_type)
        for tool_type in tool_types:
            print(f"Tools of type '{tool_type}':")
            tools_of_type = self.get_tools_by_type(tool_type)
            for tool in tools_of_type:
                print(tool)
            print("-" * 20)

    def get_tools(self) -> List[Tool]:
        """Returns a list of all tools."""
        return list(self.tools.values())

# --- Example Usage ---
if __name__ == "__main__":
    tools_dir = "tools"  # Replace with the actual path to your tools directory
    tool_manager = ToolManager(tools_dir)

    # Access tools by type
    file_tools = tool_manager.get_tools_by_type("file_operation")
    print("File tools:", file_tools)

    # Access tools by description
    search_tools = tool_manager.get_tools_by_description("something specific")
    print("Search tools:", search_tools)

    # Access a specific tool by name
    read_tool = tool_manager.get_tool("my_tool_function")  # Assuming your tool is named "my_tool_function"
    print("Read tool:", read_tool)

    # Get all tools
    all_tools = tool_manager.get_tools()
    print("All tools:", all_tools)