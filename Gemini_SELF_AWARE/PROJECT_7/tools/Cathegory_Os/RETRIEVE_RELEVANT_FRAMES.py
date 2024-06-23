import asyncio
import sys
from typing import List, Dict, Any

from SelAwareAI_Gemini.Gemini_SELF_AWARE.PROJECT_7 import SomeMemoryScript______MemoryRetrival as M



async def RETRIEVE_RELEVANT_FRAMES(query: str, top_n: int = 5) -> List[Dict[str, Any]]:
    print(f"RETRIEVE_RELEVANT_FRAMES entered query = {query}")
    result = await M.RETRIEVE_RELEVANT_FRAMES(query, top_n)
    if result is not None:
        return result
    else:
        return ["__"]


RETRIEVE_RELEVANT_FRAMES_description_json = {
    "function_declarations": [
        {
            "name": "RETRIEVE_RELEVANT_FRAMES",
            "description": "Core function to retrieve relevant frames based on a query. It loads memory frames, computes embeddings if needed, performs the search, and returns the results with detailed information.",
            "parameters": {
                "type_": "OBJECT",
                "properties": {
                    "query": {
                        "type_": "STRING",
                        "description": "The query string to search for memory."
                    },
                    "top_n": {
                        "type_": "INTEGER",
                        "description": "Number of top relevant frames to retrieve."
                    }
                },
            },
        },
    ]
}

RETRIEVE_RELEVANT_FRAMES_description_short_str = "Retrieves Memory Frames"

tool_type_for_Tool_Manager = "input"