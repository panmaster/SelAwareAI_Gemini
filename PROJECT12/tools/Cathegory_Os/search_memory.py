tool_type_for_Tool_Manager="all"

import os
import json
import logging
import re
from datetime import datetime, time
from functools import lru_cache
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import List, Dict, Union, Optional, Tuple, Literal

from fuzzywuzzy import fuzz

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Define types for filter criteria
ImportanceFilter = Union[int, Dict[Literal["min", "max", "above", "below"], int]]
EmotionFilter = Dict[str, Dict[Literal["minimum", "maximum"], float]]
ContentFilter = Dict[str, Union[str, List[str]]]
DateRange = Tuple[str, str]  # Use Tuple for fixed-length range
TimeRange = Tuple[str, str]  # Use Tuple for fixed-length range


def search_memory(
        query: str,
        max_results: int = 5,
        max_iterations: int = 3,  # Currently unused, consider adding adaptive search
        importance_filter: Optional[ImportanceFilter] = None,
        keyword_filter: Optional[List[str]] = None,
        return_fields: Optional[List[str]] = None,
        category: Optional[str] = None,
        subcategory: Optional[str] = None,
        emotion_filter: Optional[EmotionFilter] = None,
        content_filter: Optional[ContentFilter] = None,
        timestamp_range: Optional[DateRange] = None,
        session_time_range: Optional[TimeRange] = None
) -> List[Dict]:
    """
    Searches memory frames based on provided criteria.

    Args:
        query: The search query string.
        max_results: The maximum number of results to return.
        max_iterations: The maximum number of iterations for adaptive search (not yet implemented).
        importance_filter: Filter results by importance level (0-100). It can be a single value or a dictionary specifying a range.
        keyword_filter: Filter results by keywords. Provide a list of keywords to match in the content.
        return_fields: Specify fields to extract from each memory frame. Only the specified fields will be included in the result.
        category: Filter results by category. Matches the 'category' field in the memory frame.
        subcategory: Filter results by subcategory. Matches the 'subcategory' field in the memory frame.
        emotion_filter: Filter results based on emotion values. Provide a dictionary with emotion names and their value ranges.
        content_filter: Filter results based on specific content fields. Provide a dictionary with field names and expected values.
        timestamp_range: Filter results by timestamp range in 'YYYY-MM-DD' format. Provide a tuple with start and end dates.
        session_time_range: Filter results by session time range in 'HH:MM:SS' format. Provide a tuple with start and end times.

    Returns:
        List of matching memory frames with their relevance scores.
    """
    searcher = MemoryFrameSearcher()
    results = searcher.search_memory_frames(
        query=query,
        max_results=max_results,
        importance_filter=importance_filter,
        keyword_filter=keyword_filter,
        return_fields=return_fields,
        category=category,
        subcategory=subcategory,
        emotion_filter=emotion_filter,
        content_filter=content_filter,
        timestamp_range=timestamp_range,
        session_time_range=session_time_range
    )

    for result in results:
        print(f"File: {result['file_path']}")
        print(f"Score: {result['score']}")
        print(f"Main Topic: {result['data'].get('memory_data', {}).get('engine', {}).get('main_topic', 'N/A')}")
        print(
            f"Concise Summary: {result['data'].get('memory_data', {}).get('summary', {}).get('concise_summary', 'N/A')}")
        print("---")

    return results


# --- Tool Description for Agents/Interfaces ---
search_memory_description_json = {
    "name": "search_memory",
    "description": "Searches memory frames within a specified folder based on provided criteria.",
    "parameters": {
        "type_": "OBJECT",
        "properties": {
            "query": {
                "type_": "STRING",
                "description": "The search query string."
            },
            "max_results": {
                "type_": "INTEGER",
                "description": "The maximum number of results to return. Defaults to 5."
            },
            "importance_filter": {
                "type_": "OBJECT",
                "description": "Filter results by importance level (0-100). Provide a single value or a dictionary specifying 'minimum', 'maximum', 'above', and 'below' ranges.",
                "properties": {
                    "minimum": {
                        "type_": "INTEGER",
                        "description": "Minimum importance level (inclusive)."
                    },
                    "maximum": {
                        "type_": "INTEGER",
                        "description": "Maximum importance level (inclusive)."
                    },
                    "above": {
                        "type_": "INTEGER",
                        "description": "Return results with importance above this value."
                    },
                    "below": {
                        "type_": "INTEGER",
                        "description": "Return results with importance below this value."
                    }
                }
            },
            "keyword_filter": {
                "type_": "ARRAY",
                "items": {
                    "type_": "STRING"
                },
                "description": "Filter results by keywords. Example: ['keyword1', 'keyword2']."
            },
            "return_fields": {
                "type_": "ARRAY",
                "items": {
                    "type_": "STRING"
                },
                "description": "Specify fields to extract from each memory frame."
            },
            "category": {
                "type_": "STRING",
                "description": "Filter results by category."
            },
            "subcategory": {
                "type_": "STRING",
                "description": "Filter results by subcategory."
            },
            "emotion_filter": {
                "type_": "OBJECT",
                "description": "Filter results based on emotion values. Provide a dictionary with emotion names and their value ranges.",
                "properties": {
                    "happy": {
                        "type_": "OBJECT",
                        "properties": {
                            "minimum": {
                                "type_": "NUMBER",
                                "description": "Minimum emotion value (inclusive)."
                            },
                            "maximum": {
                                "type_": "NUMBER",
                                "description": "Maximum emotion value (inclusive)."
                            }
                        },
                        "required": [
                            "minimum",
                            "maximum"
                        ]
                    }
                }
            },
            "content_filter": {
                "type_": "OBJECT",
                "description": "Filter results based on specific content fields. Provide a dictionary with field names and expected values.",
                "properties": {
                    "weather": {
                        "type_": "STRING"
                    },
                    "location": {
                        "type_": "ARRAY",
                        "items": {
                            "type_": "STRING"
                        }
                    }
                }
            },
            "timestamp_range": {
                "type_": "ARRAY",
                "items": {
                    "type_": "STRING"
                },
                "description": "Filter results by timestamp range in 'YYYY-MM-DD' format. Must contain exactly two elements: [start_date, end_date].",

            },
            "session_time_range": {
                "type_": "ARRAY",
                "items": {
                    "type_": "STRING"
                },
                "description": "Filter results by session time range in 'HH:MM:SS' format. Must contain exactly two elements: [start_time, end_time].",

            }
        },
        "required": [
            "query"
        ]
    }
}


search_memory_description_short_str = 'Searches memory frames within a specified folder based on provided criteria.'


class MemoryFrameSearcher:
    def __init__(self, memories_folder_path: str = "../../memory/AiGenerated"):
        self.memories_folder_path = memories_folder_path

    @lru_cache(maxsize=1000)
    def _parse_filename(self, filename: str) -> Dict[str, Union[str, int]]:
        """Parse memory frame filename and cache the result."""
        pattern = r"MemoryFrame___Session_(\d{2}-\d{2}-\d{2})___(\d{4}-\d{2}-\d{2}_\d{2}-\d{2})___importance___(\d{3})___(.+)\.json"
        match = re.match(pattern, filename)
        if match:
            return {
                'session_time': match.group(1),
                'timestamp': match.group(2),
                'importance': int(match.group(3)),
                'title': match.group(4)
            }
        return {}

    def _apply_filters(
            self,
            memory_frame: Dict,
            file_info: Dict[str, Union[str, int]],
            filters: Dict[str, Union[ImportanceFilter, DateRange, List[str], str, EmotionFilter, ContentFilter]]
    ) -> bool:
        """Apply all filters to a memory frame."""
        for filter_name, filter_value in filters.items():
            filter_method = getattr(self, f"_filter_{filter_name}", None)
            if filter_method and not filter_method(memory_frame, file_info, filter_value):
                return False
        return True

    def _filter_importance(
            self,
            memory_frame: Dict,
            file_info: Dict[str, Union[str, int]],
            importance_filter: ImportanceFilter
    ) -> bool:
        importance = file_info['importance']
        if isinstance(importance_filter, int):
            return importance == importance_filter
        elif isinstance(importance_filter, dict):
            return all([
                importance >= importance_filter.get('min', importance),
                importance <= importance_filter.get('max', importance),
                importance > importance_filter.get('above', importance - 1),
                importance < importance_filter.get('below', importance + 1)
            ])
        return True

    def _filter_timestamp(
            self,
            memory_frame: Dict,
            file_info: Dict[str, Union[str, int]],
            timestamp_range: DateRange
    ) -> bool:
        timestamp = datetime.strptime(file_info['timestamp'], "%Y-%m-%d_%H-%M")
        start_date = datetime.strptime(timestamp_range[0], "%Y-%m-%d")
        end_date = datetime.strptime(timestamp_range[1], "%Y-%m-%d")
        return start_date <= timestamp <= end_date

    def _filter_keyword(
            self,
            memory_frame: Dict,
            file_info: Dict[str, Union[str, int]],
            keyword_filter: List[str]
    ) -> bool:
        content = json.dumps(memory_frame)
        return any(keyword.lower() in content.lower() for keyword in keyword_filter)

    def _filter_category(
            self,
            memory_frame: Dict,
            file_info: Dict[str, Union[str, int]],
            category: str
    ) -> bool:
        return memory_frame.get('memory_data', {}).get('engine', {}).get('category') == category

