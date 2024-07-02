import ast
from google import generativeai
import google.generativeai as genai

def InitialiseModel(self, model_name=None, tool_type=None, instruction=None):
    try:
        alltools_str = self.tool_manager.get_tools_list_json(tool_type)
        alltools = ast.literal_eval(alltools_str)
        if model_name is None:
            model_name = "gemini-1.5-flash-latest"
        elif model_name == "gemini-pro":
            model_name = "gemini-1.5-pro"
        else:
            raise ValueError("Invalid model_name: {}".format(model_name))
        if instruction is None:
            instruction = """
                         You are an AI assistant 
                         """

        self.input_model = genai.GenerativeModel(
            system_instruction=instruction,
            model_name=model_name,
            tools=alltools,
            safety_settings={"HARASSMENT": "block_none"})

        self.input_chat = self.input_model.start_chat(history=[])

    except Exception as E:
        print("faild to initialise  input  model")
        print(E)