import os
import importlib.util
import json
from typing import Dict, List


class ToolManager:
    def __init__(self, tools_directory="tools"):
        print(f"\033[92mInitializing ToolManager with tools directory: {tools_directory}\033[0m")
        self.tools_directory = tools_directory
        self.tool_mapping = {}
        self.all_tools = []
        self.short_descriptions = {}
        self.categories = {}
        self.tool_types = {}
        self.valid_tool_types = {"all", "input", "reflection", "action", "web"}
        self._load_tools()

    def _load_tools(self):
        print(f"\033[92mScanning tools directory: {self.tools_directory}\033[0m")
        for category in os.listdir(self.tools_directory):
            print(f"  \033[94mFound category: {category}\033[0m")
            category_path = os.path.join(self.tools_directory, category)
            if os.path.isdir(category_path):
                self.categories[category] = {"tools": []}
                for filename in os.listdir(category_path):
                    if filename.endswith(".py") and not filename.startswith("_"):
                        print(f"    \033[96m- Found Python file: {filename}\033[0m")
                        tool_name = filename[:-3]
                        self._load_tool(category, tool_name)
                        self.categories[category]["tools"].append(tool_name)

    def _load_tool(self, category, tool_name):
        print(f"    \033[96m- Loading tool: {tool_name} from category: {category}\033[0m")
        module_name = f"{category}.{tool_name}"
        module_path = os.path.join(self.tools_directory, category, f"{tool_name}.py")
        spec = importlib.util.spec_from_file_location(module_name, module_path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)

        tool_function = getattr(module, tool_name, None)
        description_name = f"{tool_name}_description_json"
        tool_description = getattr(module, description_name, None)
        tool_type = getattr(module, "tool_type_for_Tool_Manager", "all")

        if tool_function is not None and tool_description is not None:
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
            print(f"      \033[93m- Tool type: {tool_type}\033[0m")
        else:
            print(f"      \033[91m- Warning: Could not load tool function or description for '{tool_name}' from '{module_path}'\033[0m")

    def get_tools_list_json(self, tool_type: str = "all") -> str:
        filtered_tools = self.get_filtered_tools(tool_type)
        return json.dumps(filtered_tools, indent=2)

    def get_filtered_tools(self, tool_type: str = "all") -> List[Dict]:
        if tool_type not in self.valid_tool_types:
            print(f"\033[91mWarning: Invalid tool type '{tool_type}'. Using 'all' instead.\033[0m")
            tool_type = "all"

        return [tool for tool in self.all_tools if tool_type == "all" or tool["type"] == tool_type]

    def get_tools_structure(self):
        return {
            "categories": self.categories,
            "all_tools": self.all_tools,
            "tool_mapping": self.tool_mapping,
            "short_descriptions": self.short_descriptions,
            "tool_types": self.tool_types
        }

    def print_tools_structure(self):
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
            print(f"  \033[93m{i}. {tool['name']}: {json.dumps(tool['description'], indent=2)}\033[0m")
        print(f"\n\n\033[92mTool Types:\033[0m")
        for tool_name, tool_type in tools_structure["tool_types"].items():
            print(f"  \033[96m- {tool_name}: {tool_type}\033[0m")
        print(f"\n\033[93mValid tool types: {', '.join(self.valid_tool_types)}\033[0m")
        print(f"\n\n\033[95m=========================================\033[0m")
        return tools_structure


def print_tools(tools: List[Dict], tool_type: str):
    print(f"\n\033[95m{tool_type.capitalize()} Tools:\033[0m")
    if not tools:
        print(f"\033[93mNo tools found for type: {tool_type}\033[0m")
    else:
        for i, tool in enumerate(tools, 1):
            print(f"  \033[96m{i}. {tool['name']}: \033[0m{json.dumps(tool['description'], indent=2)}")


if __name__ == "__main__":
    tool_manager = ToolManager()
    tool_manager.print_tools_structure()

    for tool_type in ["all", "input", "reflection", "action", "web"]:
        filtered_tools = tool_manager.get_filtered_tools(tool_type)
        print_tools(filtered_tools, tool_type)

    print("------------------------------------------------------------------")
    all_tools_json = tool_manager.get_tools_list_json("all")
    input_tools_json = tool_manager.get_tools_list_json("input")
    reflection_tools_json = tool_manager.get_tools_list_json("reflection")

    print(f"\n\033[95mAll Tools JSON:\033[0m")
    print(all_tools_json)
    print(f"\n\033[95mInput Tools JSON:\033[0m")
    print(input_tools_json)
    print(f"\n\033[95mReflection Tools JSON:\033[0m")
    print(reflection_tools_json)

v=tool_manager.get_filtered_tools("action")