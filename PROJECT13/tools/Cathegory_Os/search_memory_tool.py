import os
import json
import logging
import re
from datetime import datetime, time
from functools import lru_cache
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import List, Dict, Union, Optional, Tuple, Literal, Any
import asyncio
from aiofiles import open as aio_open
from fuzzywuzzy import fuzz



import asyncio
from typing import Dict, Any, Optional, List, Union, Tuple, Literal


# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Define types for filter criteria
ImportanceFilter = Union[int, Dict[Literal["min", "max", "above", "below"], int]]
EmotionFilter = Dict[str, Dict[Literal["minimum", "maximum"], float]]
ContentFilter = Dict[str, Union[str, List[str]]]
DateRange = Tuple[str, str]
TimeRange = Tuple[str, str]


class SearchError(Exception):
    """Custom exception for search-related errors."""
    pass


async def search_memory_tool(args: Dict[str, Any]) -> Dict[str, Any]:
    """
    External function to be called by a tool manager or similar system.

    Args:
        args: A dictionary containing the search parameters.

    Returns:
        A dictionary containing the search results and status.
    """
    try:
        results = await search_memory(
            query=args.get('query', ''),
            max_results=args.get('max_results', 5),
            importance_filter=args.get('importance_filter'),
            keyword_filter=args.get('keyword_filter'),
            return_fields=args.get('return_fields'),
            category=args.get('category'),
            subcategory=args.get('subcategory'),
            emotion_filter=args.get('emotion_filter'),
            content_filter=args.get('content_filter'),
            timestamp_range=args.get('timestamp_range'),
            session_time_range=args.get('session_time_range')
        )

        return {
            "status": "success",
            "results": results
        }
    except SearchError as e:
        return {
            "status": "error",
            "message": str(e)
        }
    except Exception as e:
        return {
            "status": "error",
            "message": f"An unexpected error occurred: {str(e)}"
        }

# JSON description for the tool
search_memory_tool_description_json =  {
  "name": "search_memory",
  "description": "Searches the memory store for relevant information.",
  "parameters": {
    "type_": "OBJECT",
    "properties": {
      "query": {
        "type_": "STRING",
        "description": "The search query string."
      },
      "max_results": {
        "type_": "INTEGER",
        "description": "The maximum number of results to return.",

      },
      "importance_filter": {
        "type_": "STRING",
        "description": "Filter results by importance level (e.g., 'high', 'medium', 'low')."
      },
      "keyword_filter": {
        "type_": "ARRAY",
        "items": {
          "type_": "STRING"

        },
        "description": "Filter results by keywords."
      },
      "return_fields": {
        "type_": "ARRAY",
        "items": {
          "type_": "STRING"
        },
        "description": "Specify the fields to return in the results."
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
        "type_": "STRING",
        "description": "Filter results by emotion (e.g., 'happy', 'sad', 'angry')."
      },
      "content_filter": {
        "type_": "STRING",
        "description": "Filter results by content type (e.g., 'text', 'image', 'audio')."
      },
      "timestamp_range": {
        "type_": "ARRAY",
        "items": {
          "type_": "STRING",
          "description": "date-time"
        },
        "description": "Filter results by timestamp range (start, end)."
      },
      "session_time_range": {
        "type_": "ARRAY",
        "items": {
          "type_": "STRING",
          "description": "date-time"
        },
        "description": "Filter results by session time range (start, end)."
      }
    },
    "required": [
      "query"
    ]
  }
}

search_memory_tool_description_short_str = "Searches memory frames within a specified folder based on provided criteria."


async def search_memory(
        query: str,
        max_results: int = 5,
        importance_filter: Optional[ImportanceFilter] = None,
        keyword_filter: Optional[List[str]] = None,
        return_fields: Optional[List[str]] = None,
        category: Optional[str] = None,
        subcategory: Optional[str] = None,
        emotion_filter: Optional[EmotionFilter] = None,
        content_filter: Optional[ContentFilter] = None,
        timestamp_range: Optional[DateRange] = None,
        session_time_range: Optional[TimeRange] = None
) -> List[Dict[str, Any]]:
    """
    Asynchronously searches memory frames based on provided criteria.

    Args:
        (... same as before ...)

    Returns:
        List of matching memory frames with their relevance scores.

    Raises:
        SearchError: If an error occurs during the search process.
    """
    try:
        searcher = MemoryFrameSearcher()
        results = await searcher.search_memory_frames(
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
            logger.info(f"File: {result['file_path']}")
            logger.info(f"Score: {result['score']}")
            logger.info(f"Main Topic: {result['data'].get('memory_data', {}).get('core', {}).get('main_topic', 'N/A')}")
            logger.info(
                f"Concise Summary: {result['data'].get('memory_data', {}).get('summary', {}).get('concise_summary', 'N/A')}")
            logger.info("---")

        return results
    except Exception as e:
        logger.error(f"An error occurred during memory search: {str(e)}")
        raise SearchError(f"Memory search failed: {str(e)}")


class MemoryFrameSearcher:
    def __init__(self, memories_folder_path: str = "../../memories/AiGenerated"):
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
            memory_frame: Dict[str, Any],
            file_info: Dict[str, Union[str, int]],
            filters: Dict[str, Any]
    ) -> bool:
        """Apply all filters to a memory frame."""
        for filter_name, filter_value in filters.items():
            filter_method = getattr(self, f"_filter_{filter_name}", None)
            if filter_method and not filter_method(memory_frame, file_info, filter_value):
                return False
        return True




    def _filter_importance(
            self,
            memory_frame: Dict[str, Any],
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
            memory_frame: Dict[str, Any],
            file_info: Dict[str, Union[str, int]],
            timestamp_range: DateRange
    ) -> bool:
        timestamp = datetime.strptime(file_info['timestamp'], "%Y-%m-%d_%H-%M")
        start_date = datetime.strptime(timestamp_range[0], "%Y-%m-%d")
        end_date = datetime.strptime(timestamp_range[1], "%Y-%m-%d")
        return start_date <= timestamp <= end_date

    def _filter_keyword(
            self,
            memory_frame: Dict[str, Any],
            file_info: Dict[str, Union[str, int]],
            keyword_filter: List[str]
    ) -> bool:
        content = json.dumps(memory_frame)
        return any(fuzz.partial_ratio(keyword.lower(), content.lower()) > 80 for keyword in keyword_filter)

    def _filter_category(
            self,
            memory_frame: Dict[str, Any],
            file_info: Dict[str, Union[str, int]],
            category: str
    ) -> bool:
        return memory_frame.get('memory_data', {}).get('core', {}).get('category') == category

    async def _read_memory_frame(self, file_path: str) -> Dict[str, Any]:
        try:
            async with aio_open(file_path, 'r') as file:
                content = await file.read()
                return json.loads(content)
        except json.JSONDecodeError as e:
            logger.error(f"Error decoding JSON in file {file_path}: {str(e)}")
            return {}
        except Exception as e:
            logger.error(f"Error reading file {file_path}: {str(e)}")
            return {}

    def _calculate_relevance_score(self, memory_frame: Dict[str, Any], query: str) -> float:
        # Implement a more sophisticated relevance scoring mechanism
        content = json.dumps(memory_frame)
        return fuzz.token_set_ratio(query, content) / 100.0

    async def search_memory_frames(
            self,
            query: str,
            max_results: int = 5,
            **filters: Any
    ) -> List[Dict[str, Any]]:
        results = []
        tasks = []

        for filename in os.listdir(self.memories_folder_path):
            if filename.endswith('.json'):
                file_path = os.path.join(self.memories_folder_path, filename)
                file_info = self._parse_filename(filename)

                if not self._apply_filters({}, file_info, filters):
                    continue

                tasks.append(self._process_memory_frame(file_path, file_info, query, filters))

        async with asyncio.TaskGroup() as tg:
            for task in tasks:
                tg.create_task(task)

        for task in tasks:
            result = await task
            if result:
                results.append(result)

        results.sort(key=lambda x: x['score'], reverse=True)
        return results[:max_results]

    async def _process_memory_frame(
            self,
            file_path: str,
            file_info: Dict[str, Union[str, int]],
            query: str,
            filters: Dict[str, Any]
    ) -> Optional[Dict[str, Any]]:
        memory_frame = await self._read_memory_frame(file_path)

        if not self._apply_filters(memory_frame, file_info, filters):
            return None

        score = self._calculate_relevance_score(memory_frame, query)

        return {
            'file_path': file_path,
            'score': score,
            'data': memory_frame
        }

# The tool description JSON remains the same