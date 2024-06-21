
import sys
from  SelAwareAI_Gemini.Gemini_SELF_AWARE.PROJECT_4 import  SomeMemoryScript______MemoryRetrival as M
def RETRIVE_RELEVANT_FRAMES(query,Essentials="all",JSON=False):
   print("RETRIVE_RELEVANT_FRAMES entered")
   result= M.RETRIVE_RELEVANT_FRAMES(query,Essentials)
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
            "description": "The query string to search for."
          },
          "Essentials": {
            "type_": "STRING",
            "description": "Specifies the level of detail to return. Options are: 'all', 'sumarisation', 'sumarisation_OnlyExistingEntries'. Defaults to 'sumarisation_OnlyExistingEntrie'.",
            "enum": [
              "all",
              "sumarisation",
              "sumarisation_OnlyExistingEntries"
            ]
          }
        },
        "required": [
          "query"
        ]
      },

    }
  ]
}


RETRIVE_RELEVANT_FRAMES_short_str="Retrives Memory Frames "