
import sys
from  SelAwareAI_Gemini.Gemini_SELF_AWARE.PROJECT_2_refactored_testing import  SomeMemoryScript______MemoryRetrival as M
def RETRIVE_RELEVANT_FRAMES(query,Essentials="all"):
   print("RETRIVE_RELEVANT_FRAMES entered")
   result= M.RETRIEVE_RELEVANT_FRAMES(query,Essentials)
   if result is not None:
        return  result
   else:
       result="__"
       return   result






RETRIVE_RELEVANT_FRAMES_description_json = {
    "function_declarations": [
        {
            "name": "RETRIEVE_RELEVANT_FRAMES",
            "description": "Retrieves relevant frames from memory based on a query. It loads memory frames, computes embeddings if needed, performs the search, and returns the results with detailed information.",
            "parameters": {
                "type_": "OBJECT",
                "properties": {
                    "query": {
                        "type_": "STRING",
                        "description": "The query to search for relevant frames."
                    },
                    "Essentials": {
                        "type_": "STRING",
                        "description": "Specifies the level of detail to return in the results. \n\n - \"all\": Returns all available information about the relevant frames.\n - \"sumarisation\": Returns a summarised version of the frame data, including metadata, type, core, summary, content, interaction, impact, importance, and technical details.\n - \"sumarisation_OnlyExistingEntries\": Returns a summarised version of the frame data, but only includes entries that have a non-empty value.\n Defaults to \"all\".",

                    }
                },
                "required": ["query"]
            },


        }
    ]
}


RETRIVE_RELEVANT_FRAMES_short_str="Retrives Memory Frames "