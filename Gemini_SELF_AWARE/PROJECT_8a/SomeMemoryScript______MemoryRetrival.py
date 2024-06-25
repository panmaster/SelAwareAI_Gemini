import json
import os
import numpy as np
import torch
from transformers import AutoModel, AutoTokenizer
from sklearn.cluster import KMeans
from sklearn.metrics.pairwise import cosine_similarity
from typing import List, Dict, Any, Optional
import logging
import re
from datetime import datetime
import asyncio
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from nltk.stem import WordNetLemmatizer

# Setting up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Directories and constants
MEMORY_FRAMES_DIR = './memories'
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
class ImprovedMemoryRetrieval:
    def __init__(self):
        self.model = AutoModel.from_pretrained(MODEL_NAME)
        self.tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
        self.kmeans = KMeans(n_clusters=NUM_CLUSTERS, random_state=42)
        self.memory_frames: List[MemoryFrame] = []
        self.embeddings: Dict[str, Dict[str, Any]] = {}
        self.lemmatizer = WordNetLemmatizer()

    async def initialize(self):
        self.memory_frames = await self.load_memory_frames()
        self.embeddings = await self.generate_memory_embeddings(self.memory_frames)
        if self.embeddings:
            try:
                embedding_list = [emb['embedding'] for emb in self.embeddings.values()]
                if len(embedding_list) >= self.kmeans.n_clusters:
                    self.kmeans.fit(embedding_list)
                    logger.info(f"Initialization complete! Memory frames and embeddings loaded. Clustering complete with {NUM_CLUSTERS} clusters.")
                else:
                    logger.warning(f"Not enough memory frames ({len(embedding_list)}) for clustering. Need at least {self.kmeans.n_clusters}. Skipping clustering step.")
            except ValueError as e:
                logger.error(f"Error fitting KMeans: {e}")
        else:
            logger.info("Initialization complete! Memory frames and embeddings loaded.")

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

    async def generate_memory_embeddings(self, memory_frames: List[MemoryFrame]) -> Dict[str, Dict[str, Any]]:
        embeddings = {}
        for frame in memory_frames:
            try:
                parsed_name = self.parse_frame_name(frame.frame_name)
                if parsed_name:
                    combined_embedding = self.generate_combined_embedding(frame)
                    embeddings[frame.frame_name] = {
                        'embedding': combined_embedding,
                        'metadata': parsed_name
                    }
                    logger.info(f"Generated embedding for frame: {frame.frame_name}")
            except Exception as e:
                logger.error(f"Error generating embedding for frame '{frame.frame_name}': {e}")
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

    async def retrieve_relevant_memory_frames(self, query: str, top_n: int = 5, time_weight: float = 0.2,
                                              importance_weight: float = 0.3) -> List[MemoryFrame]:
        try:
            if not self.memory_frames:
                logger.warning("No memory frames loaded! Make sure to initialize properly.")
                return []

            query_embedding = self.generate_embedding(query)

            if len(self.memory_frames) < self.kmeans.n_clusters:
                logger.warning(f"Not enough memory frames ({len(self.memory_frames)}) for meaningful clustering.")
                logger.warning("Returning all frames based on similarity.")
                cluster_memories = self.memory_frames
            else:
                cluster = self.kmeans.predict([query_embedding])[0]
                cluster_memories = [frame for frame in self.memory_frames if
                                    self.kmeans.predict([self.embeddings[frame.frame_name]['embedding']])[0] == cluster]

            current_time = datetime.now()
            scored_memories = []
            for frame in cluster_memories:
                similarity = cosine_similarity([query_embedding], [self.embeddings[frame.frame_name]['embedding']])[0][0]

                parsed_name = self.parse_frame_name(frame.frame_name)
                if parsed_name:
                    try:
                        time_diff = current_time - datetime.strptime(parsed_name['timestamp'], "%Y-%m-%d_%H-%M")
                    except ValueError:
                        logger.warning(f"Invalid timestamp format in frame '{frame.frame_name}'. Using default time difference.")
                        time_diff = datetime.now() - datetime.now()

                    time_factor = 1 / (1 + time_diff.days)
                    importance_factor = parsed_name.get('importance', 0) / 100

                    adjusted_score = (
                            similarity * (1 - time_weight - importance_weight) +
                            time_factor * time_weight +
                            importance_factor * importance_weight
                    )

                    scored_memories.append((adjusted_score, frame))

            sorted_memories = sorted(scored_memories, key=lambda x: x[0], reverse=True)

            return [memory for _, memory in sorted_memories[:top_n]]
        except Exception as e:
            logger.error(f"Error retrieving relevant memory frames for query '{query}': {e}")
            return []

    async def expand_query(self, query: str) -> str:
        try:
            return query + " " + " ".join(self.tokenizer.tokenize(query))
        except Exception as e:
            logger.error(f"Error expanding query '{query}': {e}")
            return query

    async def retrieve_memories(self, query: str, top_n: int = 5) -> List[Dict[str, Any]]:
        try:
            if not self.memory_frames:
                return [{"message": "Your memory is fresh! Not enough MemoryFrames yet."}]

            if len(self.memory_frames) < self.kmeans.n_clusters:
                return self.keyword_search(query, top_n)

            expanded_query = await self.expand_query(query)
            relevant_frames = await self.retrieve_relevant_memory_frames(expanded_query, top_n)

            return [
                {
                    'frame_name': frame.frame_name,
                    'input': frame.input,
                    'response1': frame.response1,
                    'response2': frame.response2,
                    'memory_data': frame.memory_data,
                    'timestamp': frame.timestamp,
                    'edit_number': frame.edit_number
                }
                for frame in relevant_frames
            ]
        except Exception as e:
            logger.error(f"Error retrieving memories for query '{query}': {e}")
            return []

    def keyword_search(self, query: str, top_n: int = 5) -> List[MemoryFrame]:
        query_terms = [self.lemmatizer.lemmatize(term.lower()) for term in query.lower().split()]
        scored_frames = []
        for frame in self.memory_frames:
            matches = 0
            for term in query_terms:
                if term in self.lemmatizer.lemmatize(frame.input.lower()) or \
                        term in self.lemmatizer.lemmatize(frame.response1.lower()) or \
                        term in self.lemmatizer.lemmatize(frame.response2.lower()):
                    matches += 1
            score = matches * self.parse_frame_name(frame.frame_name)['probability']
            scored_frames.append((score, frame))

        sorted_frames = sorted(scored_frames, key=lambda x: x[0], reverse=True)
        return [frame for _, frame in sorted_frames[:top_n]]


memory_retrieval = ImprovedMemoryRetrieval()
app = FastAPI()

class Query(BaseModel):
    text: str
    top_n: int = 5

@app.on_event("startup")
async def startup_event():
    try:
        await memory_retrieval.initialize()
    except Exception as e:
        logger.error(f"Error during startup initialization: {e}")

@app.post("/retrieve_memories")
async def retrieve_memories_api(query: Query):
    try:
        memories = await memory_retrieval.retrieve_memories(query.text, query.top_n)
        return {"memories": memories}
    except Exception as e:
        logger.error(f"Error retrieving memories via API for query '{query.text}': {e}")
        raise HTTPException(status_code=500, detail="Internal server error")






async def RETRIEVE_RELEVANT_FRAMES(query: str, top_n: int = 5) -> List[Dict[str, Any]]:
    logger.info(f"Retrieving relevant frames for query: {query}")
    result = await memory_retrieval.retrieve_relevant_memory_frames(query, top_n)
    if result:
        return [
            {
                'frame_name': frame.frame_name,
                'input': frame.input,
                'response1': frame.response1,
                'response2': frame.response2,
                'memory_data': frame.memory_data,
                'timestamp': frame.timestamp,
                'edit_number': frame.edit_number
            }
            for frame in result
        ]
    else:
        return [{"message": "No relevant frames found."}]


if __name__ == "__main__":
    import uvicorn
    try:
        uvicorn.run(app, host="0.0.0.0", port=8000)
    except Exception as e:
        logger.error(f"Error starting the server: {e}")


