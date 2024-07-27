import asyncio
import sys
import os
import numpy as np
import torch
from transformers import AutoModel, AutoTokenizer
from sklearn.cluster import KMeans
from sklearn.metrics.pairwise import cosine_similarity
from typing import List, Dict, Any, Optional
import logging
import re
import json
from datetime import datetime
from nltk.stem import WordNetLemmatizer

# Setting up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Directories and constants
MEMORY_FRAMES_DIR = '../../memories'
EMBEDDINGS_FILE = 'memory_embeddings.npz'
MODEL_NAME = "sentence-transformers/all-mpnet-base-v2"
NUM_CLUSTERS = 10


# Memory frame class
class MemoryFrame:
    def __init__(self, frame_data: Dict, frame_name: str, frame_path: str):
        self.frame_name = frame_name
        self.frame_path = frame_path
        self.input = frame_data.get('input', '')
        self.response1 = frame_data.get('response1', '')
        self.response2 = frame_data.get('response2', '')
        self.memory_data = frame_data.get('memory_data', {})
        self.timestamp = frame_data.get('timestamp', '')
        self.edit_number = frame_data.get('edit_number', 0)


# Memory retrieval engine class
class MemoryRetrievalEngine:
    def __init__(self):
        self.model = AutoModel.from_pretrained(MODEL_NAME)
        self.tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
        self.kmeans = KMeans(n_clusters=NUM_CLUSTERS, random_state=42)
        self.memory_frames: List[MemoryFrame] = []
        self.embeddings: Dict[str, Dict[str, Any]] = {}
        self.lemmatizer = WordNetLemmatizer()

        self.load_embeddings()

    def load_embeddings(self):
        if os.path.exists(EMBEDDINGS_FILE):
            try:
                loaded_embeddings = np.load(EMBEDDINGS_FILE)
                self.embeddings = {
                    frame_name: {'embedding': embedding, 'metadata': self.parse_frame_name(frame_name)}
                    for frame_name, embedding in zip(loaded_embeddings['frame_names'], loaded_embeddings['embeddings'])
                }
                logger.info(f"Loaded embeddings from {EMBEDDINGS_FILE}")
            except Exception as e:
                logger.error(f"Error loading embeddings: {e}")

    def save_embeddings(self):
        try:
            np.savez(EMBEDDINGS_FILE,
                     frame_names=list(self.embeddings.keys()),
                     embeddings=[e['embedding'] for e in self.embeddings.values()])
            logger.info(f"Saved embeddings to {EMBEDDINGS_FILE}")
        except Exception as e:
            logger.error(f"Error saving embeddings: {e}")

    async def initialize(self):
        self.memory_frames = await self.load_memory_frames()

        new_frame_names = [frame.frame_name for frame in self.memory_frames if frame.frame_name not in self.embeddings]
        if new_frame_names:
            new_embeddings = await self.generate_memory_embeddings(new_frame_names)
            self.embeddings.update(new_embeddings)
            self.save_embeddings()

    def generate_embedding(self, text: str) -> np.ndarray:
        try:
            inputs = self.tokenizer(text, return_tensors="pt", truncation=True, padding=True, max_length=512)
            with torch.no_grad():
                outputs = self.model(**inputs)
            return outputs.last_hidden_state.mean(dim=1).squeeze().numpy()
        except Exception as e:
            logger.error(f"Error generating embedding for text '{text}': {e}")
            return np.zeros(768)

    def parse_frame_name(self, frame_name: str) -> Optional[Dict[str, Any]]:
        pattern = r"MemoryFrame__session_(\w+_\d{2}-\d{2}-\d{2})___(\d{4}-\d{2}-\d{2}_\d{2}-\d{2})___Probability_(\d+)___Importance_(\d+)___(.+)"
        match = re.match(pattern, frame_name)
        if match:
            return {
                'session_date': match.group(1),
                'timestamp': match.group(2),
                'probability': int(match.group(3)),
                'importance': int(match.group(4)),
                'topic': match.group(5)
            }
        return None

    async def load_memory_frames(self) -> List[MemoryFrame]:
        memory_frames = []
        if not os.path.exists(MEMORY_FRAMES_DIR):
            logger.warning(f"Memory frames directory not found: {MEMORY_FRAMES_DIR}")
            return memory_frames
        for root, _, files in os.walk(MEMORY_FRAMES_DIR):
            for file_name in files:
                if file_name.endswith('.json'):
                    file_path = os.path.join(root, file_name)
                    try:
                        with open(file_path, 'r') as file:
                            frame_data = json.load(file)
                            frame_name = file_name[:-5]
                            frame = MemoryFrame(frame_data, frame_name, file_path)
                            memory_frames.append(frame)
                            logger.info(f"Loaded memory frame: {frame_name}")
                    except json.JSONDecodeError as e:
                        logger.error(f"Invalid JSON in '{file_path}': {e}")
                    except Exception as e:
                        logger.error(f"Error loading memory frame '{file_name}': {e}")
        return memory_frames

    async def generate_memory_embeddings(self, frame_names: List[str]) -> Dict[str, Dict[str, Any]]:
        embeddings = {}
        for frame_name in frame_names:
            try:
                frame = next((frame for frame in self.memory_frames if frame.frame_name == frame_name), None)
                if frame:
                    combined_embedding = self.generate_combined_embedding(frame)
                    embeddings[frame_name] = {
                        'embedding': combined_embedding,
                        'metadata': self.parse_frame_name(frame_name)
                    }
                    logger.info(f"Generated embedding for frame: {frame_name}")
            except Exception as e:
                logger.error(f"Error generating embedding for frame '{frame_name}': {e}")
        return embeddings

    def generate_combined_embedding(self, frame: MemoryFrame) -> np.ndarray:
        try:
            input_embedding = self.generate_embedding(frame.input)
            response_embedding = self.generate_embedding(frame.response1 + " " + frame.response2)
            memory_data_embedding = self.generate_embedding(json.dumps(frame.memory_data))
            return np.concatenate([input_embedding, response_embedding, memory_data_embedding])
        except Exception as e:
            logger.error(f"Error generating combined embedding for frame '{frame.frame_name}': {e}")
            return np.zeros(768 * 3)

    async def retrieve_relevant_memory_frames(self, query: str, top_n: int = 5) -> List[MemoryFrame]:
        try:
            if not self.memory_frames:
                logger.warning("No memory frames loaded!")
                return []

            query_embedding = self.generate_embedding(query)

            if len(self.memory_frames) < self.kmeans.n_clusters:
                logger.warning(f"Not enough memory frames ({len(self.memory_frames)}) for meaningful clustering.")
                cluster_memories = self.memory_frames
            else:
                cluster = self.kmeans.predict([query_embedding])[0]
                cluster_memories = [frame for frame in self.memory_frames if
                                    self.kmeans.predict([self.embeddings[frame.frame_name]['embedding']])[0] == cluster]

            similarities = cosine_similarity([query_embedding],
                                             [self.embeddings[frame.frame_name]['embedding'] for frame in
                                              cluster_memories])[0]
            sorted_indices = np.argsort(similarities)[::-1]

            return [cluster_memories[i] for i in sorted_indices[:top_n]]
        except Exception as e:
            logger.error(f"Error retrieving relevant memory frames for query '{query}': {e}")
            return []

    async def expand_query(self, query: str) -> str:
        try:
            return query + " " + " ".join(self.tokenizer.tokenize(query))
        except Exception as e:
            logger.error(f"Error expanding query '{query}': {e}")
            return query


def get_nested_value(data: Dict[str, Any], keys: List[str]) -> Any:
    """Retrieve a nested value from a dictionary using a list of keys."""
    for key in keys:
        if isinstance(data, dict) and key in data:
            data = data[key]
        else:
            return None
    return data


async def retrieve_memory_parts(query: str, top_n: int = 5, fields: List[str] = None, **kwargs) -> List[Dict[str, Any]]:
    memory_retrieval = MemoryRetrievalEngine()
    await memory_retrieval.initialize()

    # If no specific fields are requested, use all fields
    if not fields:
        fields = [
            'metadata.creation_date', 'metadata.source', 'metadata.author',
            'type',
            'engine.main_topic', 'engine.category', 'engine.subcategory', 'engine.memory_about',
            'summary.concise_summary', 'summary.description',
            'content.keywords', 'content.entities', 'content.tags', 'content.observations',
            'content.facts', 'content.contradictions', 'content.paradoxes',
            'content.scientific_data', 'content.visualizations',
            'interaction.interaction_type', 'interaction.people', 'interaction.objects',
            'interaction.animals', 'interaction.actions', 'interaction.observed_interactions',
            'impact.obtained_knowledge', 'impact.positive_impact', 'impact.negative_impact',
            'impact.expectations', 'impact.strength_of_experience',
            'importance.reason', 'importance.potential_uses', 'importance.importance_level',
            'technical_details.problem_solved', 'technical_details.concept_definition',
            'technical_details.implementation_steps', 'technical_details.tools_and_technologies',
            'technical_details.example_projects', 'technical_details.best_practices',
            'technical_details.common_challenges', 'technical_details.debugging_tips',
            'technical_details.related_concepts', 'technical_details.resources',
            'technical_details.code_examples',
            'storage.storage_method', 'storage.location', 'storage.memory_folders_storage',
            'storage.strength_of_matching_memory_to_given_folder',
            'naming_suggestion.memory_frame_name', 'naming_suggestion.explanation'
        ]

    # Perform the search
    relevant_frames = await memory_retrieval.retrieve_relevant_memory_frames(query, top_n)

    # Extract only the requested fields from each relevant frame
    results = []
    for frame in relevant_frames:
        frame_data = {}
        for field in fields:
            value = get_nested_value(frame.memory_data, field.split('.'))
            if value is not None:
                frame_data[field] = value
        if frame_data:
            results.append(frame_data)

    return results


async def main():
    query = "memory enhancement system"
    fields = [
        'engine.main_topic',
        'summary.concise_summary',
        'importance.importance_level',
        'technical_details.concept_definition',
        'technical_details.common_challenges'
    ]
    results = await retrieve_memory_parts(query, top_n=3, fields=fields)

    print(f"Query: {query}")
    if results:
        print(f"Found {len(results)} relevant memory:")
        for i, result in enumerate(results, 1):
            print(f"Memory {i}:")
            print(json.dumps(result, indent=2))
    else:
        print("No relevant memory found.")



# Description for documentation
retrieve_memory_parts_description_json = {
    "function_declarations": [
        {
            "name": "retrieve_memory_partss",
            "description": "Searches memory frames based on a query and returns the top N relevant frames.",
            "parameters": {
                "type_": "OBJECT",
                "properties": {
                    "query": {
                        "type_": "STRING",
                        "description": "The query string to search for."
                    },
                    "top_n": {
                        "type_": "INTEGER",
                        "description": "The number of top results to return."
                    },
                    "time_weight": {
                        "type_": "NUMBER",
                        "description": "Weight for recency of the memory frame."
                    },
                    "importance_weight": {
                        "type_": "NUMBER",
                        "description": "Weight for importance of the memory frame."
                    },
                    "creation_date": {
                        "type_": "STRING",
                        "description": "The creation date of the memory frame to filter by."
                    },
                    "source": {
                        "type_": "STRING",
                        "description": "The source of the memory frame to filter by."
                    },
                    "author": {
                        "type_": "STRING",
                        "description": "The author of the memory frame to filter by."
                    },
                    "type": {
                        "type_": "STRING",
                        "description": "The type of the memory frame to filter by (e.g., 'conversation', 'technical_concept')."
                    },
                    "main_topic": {
                        "type_": "STRING",
                        "description": "The main topic of the memory frame to filter by."
                    },
                    "category": {
                        "type_": "STRING",
                        "description": "The category of the memory frame to filter by."
                    },
                    "subcategory": {
                        "type_": "STRING",
                        "description": "The subcategory of the memory frame to filter by."
                    },
                    "memory_about": {
                        "type_": "STRING",
                        "description": "The memory about the memory frame to filter by."
                    },
                    "concise_summary": {
                        "type_": "STRING",
                        "description": "The concise summary of the memory frame to filter by."
                    },
                    "description": {
                        "type_": "STRING",
                        "description": "The description of the memory frame to filter by."
                    },
                    "keywords": {
                        "type_": "ARRAY",
                        "description": "A list of keywords to filter by."
                    },
                    "entities": {
                        "type_": "ARRAY",
                        "description": "A list of entities to filter by."
                    },
                    "tags": {
                        "type_": "ARRAY",
                        "description": "A list of tags to filter by."
                    },
                    "observations": {
                        "type_": "ARRAY",
                        "description": "A list of observations to filter by."
                    },
                    "facts": {
                        "type_": "ARRAY",
                        "description": "A list of facts to filter by."
                    },
                    "contradictions": {
                        "type_": "ARRAY",
                        "description": "A list of contradictions to filter by."
                    },
                    "paradoxes": {
                        "type_": "ARRAY",
                        "description": "A list of paradoxes to filter by."
                    },
                    "scientific_data": {
                        "type_": "ARRAY",
                        "description": "A list of scientific data to filter by."
                    },
                    "visualizations": {
                        "type_": "ARRAY",
                        "description": "A list of visualizations to filter by."
                    },
                    "interaction_type": {
                        "type_": "ARRAY",
                        "description": "A list of interaction types to filter by."
                    },
                    "people": {
                        "type_": "ARRAY",
                        "description": "A list of people to filter by."
                    },
                    "objects": {
                        "type_": "ARRAY",
                        "description": "A list of objects to filter by."
                    },
                    "animals": {
                        "type_": "ARRAY",
                        "description": "A list of animals to filter by."
                    },
                    "actions": {
                        "type_": "ARRAY",
                        "description": "A list of actions to filter by."
                    },
                    "observed_interactions": {
                        "type_": "ARRAY",
                        "description": "A list of observed interactions to filter by."
                    },
                    "obtained_knowledge": {
                        "type_": "STRING",
                        "description": "The obtained knowledge from the memory frame to filter by."
                    },
                    "positive_impact": {
                        "type_": "STRING",
                        "description": "The positive impact of the memory frame to filter by."
                    },
                    "negative_impact": {
                        "type_": "STRING",
                        "description": "The negative impact of the memory frame to filter by."
                    },
                    "expectations": {
                        "type_": "STRING",
                        "description": "The expectations from the memory frame to filter by."
                    },
                    "strength_of_experience": {
                        "type_": "STRING",
                        "description": "The strength of the experience from the memory frame to filter by."
                    },
                    "reason": {
                        "type_": "STRING",
                        "description": "The reason for the importance of the memory frame to filter by."
                    },
                    "potential_uses": {
                        "type_": "ARRAY",
                        "description": "A list of potential uses of the memory frame to filter by."
                    },
                    "importance_level": {
                        "type_": "STRING",
                        "description": "The importance level of the memory frame (0-100) to filter by."
                    },
                    "problem_solved": {
                        "type_": "STRING",
                        "description": "The problem solved by the memory frame to filter by."
                    },
                    "concept_definition": {
                        "type_": "STRING",
                        "description": "The concept definition from the memory frame to filter by."
                    },
                    "implementation_steps": {
                        "type_": "ARRAY",
                        "description": "A list of implementation steps from the memory frame to filter by."
                    },
                    "tools_and_technologies": {
                        "type_": "ARRAY",
                        "description": "A list of tools and technologies from the memory frame to filter by."
                    },
                    "example_projects": {
                        "type_": "ARRAY",
                        "description": "A list of example projects from the memory frame to filter by."
                    },
                    "best_practices": {
                        "type_": "ARRAY",
                        "description": "A list of best practices from the memory frame to filter by."
                    },
                    "common_challenges": {
                        "type_": "ARRAY",
                        "description": "A list of common challenges from the memory frame to filter by."
                    },
                    "debugging_tips": {
                        "type_": "ARRAY",
                        "description": "A list of debugging tips from the memory frame to filter by."
                    },
                    "related_concepts": {
                        "type_": "ARRAY",
                        "description": "A list of related concepts from the memory frame to filter by."
                    },
                    "resources": {
                        "type_": "ARRAY",
                        "description": "A list of resources from the memory frame to filter by."
                    },
                    "code_examples": {
                        "type_": "ARRAY",
                        "description": "A list of code examples from the memory frame to filter by."
                    },
                    "storage_method": {
                        "type_": "STRING",
                        "description": "The storage method of the memory frame to filter by."
                    },
                    "location": {
                        "type_": "STRING",
                        "description": "The location of the memory frame to filter by."
                    },
                    "memory_folders_storage": {
                        "type_": "ARRAY",
                        "description": "A list of memory folders and probabilities to filter by."
                    },
                    "strength_of_matching_memory_to_given_folder": {
                        "type_": "ARRAY",
                        "description": "A list of strength of matching memory to given folder to filter by."
                    },
                    "memory_frame_name": {
                        "type_": "STRING",
                        "description": "The memory frame name to filter by."
                    },
                    "explanation": {
                        "type_": "STRING",
                        "description": "The explanation of the memory frame name to filter by."
                    }
                },
            },
        },
    ]
}

retrieve_memory_parts_description_short_str = "Searches Memory Frames"



if __name__ == "__main__":
    asyncio.run(main())