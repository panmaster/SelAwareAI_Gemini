tool_type_for_Tool_Manager="reflection"

from SelAwareAI_Gemini.Gemini_SELF_AWARE.PROJECT_6.PROJECT_5 import SomeMemoryScript______MemoryRetrival as M


def RETRIVE_RELEVANT_FRAMES(query):
   print(f"RETRIVE_RELEVANT_FRAMES entered query =  {query}")
   result= M.RETRIVE_RELEVANT_FRAMES(query)
   if result is not None:
        return  result
   else:
       result="__"
       return   result







RETRIVE_RELEVANT_FRAMES_description_json = {
  "function_declarations": [
    {
      "name": "RETRIVE_RELEVANT_FRAMES",
      "description": "Core function to retrieve relevant frames based on a query. It loads memory frames, computes embeddings if needed, performs the search, and returns the results with detailed information.",
      "parameters": {
        "type_": "OBJECT",
        "properties": {
          "query": {
            "type_": "STRING",
            "description": "The query string to search for memory."
          },
        },
      },
    },
  ]
}


RETRIVE_RELEVANT_FRAMES_description_short_str="Retrives Memory Frames "