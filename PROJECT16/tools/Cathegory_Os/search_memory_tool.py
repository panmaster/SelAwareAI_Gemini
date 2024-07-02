import os
import json
import logging
import re
from datetime import datetime
from functools import lru_cache
from typing import List, Dict, Union, Optional, Tuple, Literal, Any
from fuzzywuzzy import fuzz
from rank_bm25 import BM25Okapi

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

ImportanceFilter = Union[int, Dict[Literal["min", "max", "above", "below"], int]]
EmotionFilter = Dict[str, Dict[Literal["minimum", "maximum"], float]]
ContentFilter = Dict[str, Union[str, List[str]]]
DateRange = Tuple[str, str]
TimeRange = Tuple[str, str]


class SearchError(Exception):
    pass


def search_memory_tool(
        query: str,
        query_type: str = "keyword",
        query_fields: Optional[List[str]] = None,
        query_operator: str = "AND",
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
) -> Dict[str, Any]:
    try:
        results = search_memory(
            query=query,
            query_type=query_type,
            query_fields=query_fields,
            query_operator=query_operator,
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
        return {"status": "success", "results": results}
    except SearchError as e:
        return {"status": "error", "message": str(e)}
    except Exception as e:
        logger.error(f"An unexpected error occurred in search_memory_tool: {str(e)}")
        return {"status": "error", "message": f"An unexpected error occurred: {str(e)}"}


search_memory_tool_description_json = {
    "name": "search_memory_tool",
    "description": "Searches the memory store for relevant information using various querying options.",
    "parameters": {
        "type_": "OBJECT",
        "properties": {
            "query": {"type_": "STRING", "description": "The search query string."},
            "query_type": {"type_": "STRING",
                           "description": "The type of query to perform. Options are: 'keyword', 'semantic', 'regex'. Defaults to 'keyword'."},
            "query_fields": {"type_": "ARRAY", "items": {"type_": "STRING"},
                             "description": "Specify the fields to search within the memory frames."},
            "query_operator": {"type_": "STRING",
                               "description": "Logical operator for multiple query terms ('AND', 'OR'). Defaults to 'AND'. Applies only to 'keyword' query type."},
            "max_results": {"type_": "INTEGER",
                            "description": "The maximum number of results to return. Defaults to 5."},
            "importance_filter": {"type_": "STRING",
                                  "description": "Filter results by importance level (e.g., 'high', 'medium', 'low', '3', '{\"min\": 2}')."},
            "keyword_filter": {"type_": "ARRAY", "items": {"type_": "STRING"},
                               "description": "Filter results by keywords."},
            "return_fields": {"type_": "ARRAY", "items": {"type_": "STRING"},
                              "description": "Specify the fields to return in the results."},
            "category": {"type_": "STRING", "description": "Filter results by category."},
            "subcategory": {"type_": "STRING", "description": "Filter results by subcategory."},
            "emotion_filter": {"type_": "STRING",
                               "description": "Filter results by emotion (e.g., 'happy', '{\"sad\": {\"minimum\": 0.7}}')."},
            "content_filter": {"type_": "STRING",
                               "description": "Filter results by content type (e.g., 'text', 'image', 'audio')."},
            "timestamp_range": {"type_": "ARRAY", "items": {"type_": "STRING", "description": "date-time"},
                                "description": "Filter results by timestamp range (start, end)."},
            "session_time_range": {"type_": "ARRAY", "items": {"type_": "STRING", "description": "date-time"},
                                   "description": "Filter results by session time range (start, end)."}
        },
        "required": ["query"]
    }
}

search_memory_tool_description_short_str = "Searches memory frames within a specified folder based on provided criteria, using various querying options including keyword, semantic, and regex search."


def search_memory(
        query: str,
        query_type: str = "keyword",
        query_fields: Optional[List[str]] = None,
        query_operator: str = "AND",
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
    try:
        searcher = MemoryFrameSearcher()
        results = searcher.search_memory_frames(
            query=query,
            query_type=query_type,
            query_fields=query_fields,
            query_operator=query_operator,
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
            logger.info(f"Main Topic: {result['data'].get('memory_data', {}).get('engine', {}).get('main_topic', 'N/A')}")
            logger.info(
                f"Concise Summary: {result['data'].get('memory_data', {}).get('summary', {}).get('concise_summary', 'N/A')}")
            logger.info("---")

        return results
    except Exception as e:
        logger.error(f"An error occurred during memory search: {str(e)}")
        raise SearchError(f"Memory search failed: {str(e)}")


class MemoryFrameSearcher:
    def __init__(self, memories_folder_path: str = "../../memory/AiGenerated"):
        self.memories_folder_path = memories_folder_path
        self.bm25_index = None

    @lru_cache(maxsize=1000)
    def _parse_filename(self, filename: str) -> Dict[str, Union[str, int]]:
        pattern = r"MemoryFrame___Session_(\d{2}-\d{2}-\d{2})___(\d{4}-\d{2}-\d2_\d{2}-\d{2})___importance___(\d{3})___(.+)\.json"
        match = re.match(pattern, filename)
        if match:
            return {
                'session_time': match.group(1),
                'timestamp': match.group(2),
                'importance': int(match.group(3)),
                'title': match.group(4)
            }
        return {}

    def _apply_filters(self, memory_frame: Dict[str, Any], file_info: Dict[str, Union[str, int]],
                       filters: Dict[str, Any]) -> bool:
        for filter_name, filter_value in filters.items():
            filter_method = getattr(self, f"_filter_{filter_name}", None)
            if filter_method and not filter_method(memory_frame, file_info, filter_value):
                return False
        return True

    def _filter_importance(self, memory_frame: Dict[str, Any], file_info: Dict[str, Union[str, int]],
                           importance_filter: ImportanceFilter) -> bool:
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

    def _filter_timestamp(self, memory_frame: Dict[str, Any], file_info: Dict[str, Union[str, int]],
                          timestamp_range: DateRange) -> bool:
        timestamp = datetime.strptime(file_info['timestamp'], "%Y-%m-%d_%H-%M")
        start_date = datetime.strptime(timestamp_range[0], "%Y-%m-%d")
        end_date = datetime.strptime(timestamp_range[1], "%Y-%m-%d")
        return start_date <= timestamp <= end_date

    def _filter_keyword(self, memory_frame: Dict[str, Any], file_info: Dict[str, Union[str, int]],
                        keyword_filter: List[str]) -> bool:
        content = json.dumps(memory_frame)
        return any(fuzz.partial_ratio(keyword.lower(), content.lower()) > 80 for keyword in keyword_filter)

    def _filter_category(self, memory_frame: Dict[str, Any], file_info: Dict[str, Union[str, int]],
                         category: str) -> bool:
        return memory_frame.get('memory_data', {}).get('engine', {}).get('category') == category

    def _filter_subcategory(self, memory_frame: Dict[str, Any], file_info: Dict[str, Union[str, int]],
                         subcategory: str) -> bool:
        return memory_frame.get('memory_data', {}).get('engine', {}).get('subcategory') == subcategory

    def _read_memory_frame(self, file_path: str) -> Dict[str, Any]:
        try:
            with open(file_path, 'r') as file:
                content = file.read()
                return json.loads(content)
        except json.JSONDecodeError as e:
            logger.error(f"Error decoding JSON in file {file_path}: {str(e)}")
            return {}
        except Exception as e:
            logger.error(f"Error reading file {file_path}: {str(e)}")
            return {}

    def _calculate_relevance_score(self, memory_frame: Dict[str, Any], query: str, query_type: str = 'keyword',
                                   query_fields: Optional[List[str]] = None, query_operator: str = 'AND') -> float:
        if query_fields is None:
            content = json.dumps(memory_frame)
        else:
            content = " ".join([str(memory_frame.get(field, '')) for field in query_fields])

        if query_type == "keyword":
            if self.bm25_index:
                tokenized_query = query.lower().split()
                scores = self.bm25_index.get_scores(tokenized_query)
                return max(scores) if scores else 0.0
            else:
                words = query.lower().split()
                if query_operator == "AND":
                    return min(fuzz.partial_ratio(word, content.lower()) for word in words) / 100.0
                else:
                    return max(fuzz.partial_ratio(word, content.lower()) for word in words) / 100.0
        elif query_type == "semantic":
            return fuzz.token_set_ratio(query, content) / 100.0
        elif query_type == "regex":
            try:
                pattern = re.compile(query, re.IGNORECASE)
                return 1.0 if pattern.search(content) else 0.0
            except re.error:
                logger.error(f"Invalid regex pattern: {query}")
                return 0.0
        else:
            logger.warning(f"Invalid query_type: {query_type}. Using keyword search.")
            return self._calculate_relevance_score(memory_frame, query, 'keyword', query_fields, query_operator)

    def search_memory_frames(
            self,
            query: str,
            query_type: str = "keyword",
            query_fields: Optional[List[str]] = None,
            query_operator: str = "AND",
            max_results: int = 5,
            **filters: Any
    ) -> List[Dict[str, Any]]:
        results = []

        for filename in os.listdir(self.memories_folder_path):
            if filename.endswith('.json'):
                file_path = os.path.join(self.memories_folder_path, filename)
                file_info = self._parse_filename(filename)

                if not self._apply_filters({}, file_info, filters):
                    continue

                result = self._process_memory_frame(
                    file_path, file_info, query, query_type, query_fields, query_operator, filters)

                if result:
                    results.append(result)

        results.sort(key=lambda x: x['score'], reverse=True)
        return results[:max_results]

    def _process_memory_frame(
            self,
            file_path: str,
            file_info: Dict[str, Union[str, int]],
            query: str,
            query_type: str,
            query_fields: Optional[List[str]],
            query_operator: str,
            filters: Dict[str, Any]
    ) -> Optional[Dict[str, Any]]:
        memory_frame = self._read_memory_frame(file_path)

        if not self._apply_filters(memory_frame, file_info, filters):
            return None

        score = self._calculate_relevance_score(memory_frame, query, query_type, query_fields, query_operator)

        return {
            'file_path': file_path,
            'score': score,
            'data': memory_frame
        }