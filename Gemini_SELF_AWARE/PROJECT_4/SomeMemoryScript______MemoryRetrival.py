import json
import os
import torch
from transformers import BertTokenizer, BertModel
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
from typing import List, Dict, Any, Optional, Tuple
import logging
import colorama
from colorama import Fore, Style
import re

# Initialize colorama
colorama.init(autoreset=True)

# Constants
MEMORY_FRAMES_DIR = './memories'
EMBEDDINGS_FILE = 'memory_embeddings.npz'
LOGGING_FILE = 'memory_retrieval.log'

# Emoji constants
INFO, SUCCESS, WARNING, ERROR = "💡", "✅", "⚠️", "❌"
LOADING, SEARCH, BRAIN, SAVE = "⏳", "🔍", "🧠", "💾"

# Setup logging
logging.basicConfig(filename=LOGGING_FILE, level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')

# Initialize BERT model and tokenizer
tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')
model = BertModel.from_pretrained('bert-base-uncased')


class NumpyEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        return super().default(obj)


def pretty_print(message: str, emoji: str = INFO):
    print(f"\n{emoji} {Fore.CYAN}{message}{Style.RESET_ALL}")


class MemoryFrame:
    def __init__(self, frame_data: Dict, frame_name: str, frame_path: str):
        self.frame_name = frame_name
        self.frame_path = frame_path
        self.input = frame_data.get('input', 'None')
        self.response1 = frame_data.get('response1', 'None')
        self.response2 = frame_data.get('response2', 'None')
        self.memory_data = frame_data.get('memory_data', {})
        self.timestamp = frame_data.get('timestamp', 'None')
        self.edit_number = frame_data.get('edit_number', 0)

    def get_embedding(self) -> np.ndarray:
        text = json.dumps(self.__dict__)
        return get_bert_embedding(text)


def get_bert_embedding(text: str) -> np.ndarray:
    try:
        inputs = tokenizer(text, return_tensors='pt', truncation=True, padding=True, max_length=512)
        with torch.no_grad():
            outputs = model(**inputs)
        return outputs.last_hidden_state.mean(dim=1).squeeze().numpy()
    except Exception as e:
        logging.error(f"Error generating embedding: {e}")
        return np.zeros(768)


def load_memory_frames(memory_frames_dir: str) -> List[MemoryFrame]:
    pretty_print(f"Loading Memory Frames from {memory_frames_dir}...", LOADING)
    memory_frames = []
    valid_frames = invalid_frames = 0

    for root, _, files in os.walk(memory_frames_dir):
        for file_name in files:
            if file_name.endswith('.json'):
                file_path = os.path.join(root, file_name)
                try:
                    with open(file_path, 'r') as file:
                        frame_data = json.load(file)
                        frame_name = file_name[:-5]
                        frame = MemoryFrame(frame_data, frame_name, file_path)
                        if not any(existing_frame.__dict__ == frame.__dict__ for existing_frame in memory_frames):
                            memory_frames.append(frame)
                            valid_frames += 1
                        else:
                            print(f"{WARNING} {Fore.YELLOW}Duplicate frame detected: {file_name}{Style.RESET_ALL}")
                except json.JSONDecodeError as e:
                    logging.error(f"Invalid JSON in '{file_path}': {e}")
                    invalid_frames += 1

    pretty_print(f"Loaded {valid_frames} Valid Memory Frames", SUCCESS)
    if invalid_frames > 0:
        pretty_print(f"Skipped {invalid_frames} Frames with JSON Decode Errors or Duplicates", WARNING)

    return memory_frames


def generate_memory_embeddings(memory_frames: List[MemoryFrame]) -> Dict[str, np.ndarray]:
    pretty_print("Generating Embeddings", BRAIN)
    embeddings = load_embeddings()

    for i, frame in enumerate(memory_frames):
        if frame.frame_name not in embeddings:
            embeddings[frame.frame_name] = frame.get_embedding()
            if (i + 1) % 10 == 0:
                pretty_print(f"Generated embeddings for {i + 1} frames...", LOADING)

    save_embeddings(embeddings)
    pretty_print("Embeddings Generation Complete", SUCCESS)
    return embeddings


def load_embeddings() -> Dict[str, np.ndarray]:
    if os.path.exists(EMBEDDINGS_FILE):
        try:
            return dict(np.load(EMBEDDINGS_FILE))
        except Exception as e:
            logging.warning(f"Error loading embeddings: {e}")
    return {}


def save_embeddings(embeddings: Dict[str, np.ndarray]) -> None:
    try:
        np.savez_compressed(EMBEDDINGS_FILE, **embeddings)
        pretty_print(f"Embeddings saved to {EMBEDDINGS_FILE}", SAVE)
    except Exception as e:
        logging.error(f"Error saving embeddings: {e}")


def retrieve_relevant_memory_frames(
        query: str,
        retrieval_method: str,
        filter_type: str,
        top_n: int,
        update_embeddings: bool,
        included_only_filled_areas: bool,
        memory_frames: List[MemoryFrame]
) -> Dict[str, Any]:
    try:
        query_embedding = get_bert_embedding(query)
        embeddings = load_embeddings()  # Load embeddings here as well

        similarities: List[Tuple[float, MemoryFrame]] = []
        updated_embeddings = False

        for frame in memory_frames:
            frame_embedding = get_frame_embedding(frame, embeddings, update_embeddings)
            if frame_embedding is not None:
                similarity = cosine_similarity([query_embedding], [frame_embedding])[0][0]
                similarities.append((similarity, frame))
                # Always update the embeddings dictionary if update_embeddings is True
                if update_embeddings:
                    embeddings[frame.frame_name] = frame_embedding
                    updated_embeddings = True

        if updated_embeddings:
            save_embeddings(embeddings)

        similarities.sort(key=lambda x: x[0], reverse=True)
        relevant_frames = similarities[:top_n]

        result_frames = [create_result_frame(sim, frame) for sim, frame in relevant_frames]

        return {
            'relevant_frames': result_frames,
            'error': None
        }
    except Exception as e:
        logging.error(f"Error in retrieve_relevant_memory_frames: {e}")
        return {
            'relevant_frames': [],
            'error': str(e)
        }


def get_frame_embedding(frame: MemoryFrame, embeddings: Dict[str, np.ndarray], update_embeddings: bool) -> Optional[
    np.ndarray]:
    # Always regenerate the embedding if update_embeddings is True
    if update_embeddings:
        return frame.get_embedding()
    elif frame.frame_name in embeddings:
        return embeddings[frame.frame_name]
    return None


def create_result_frame(similarity: float, frame: MemoryFrame) -> Dict[str, Any]:
    return {
        'similarity_score': similarity,
        'frame_name': frame.frame_name,
        'frame_path': frame.frame_path,
        'input': frame.input,
        'response1': frame.response1,
        'response2': frame.response2,
        'memory_data': frame.memory_data,
        'timestamp': frame.timestamp,
        'edit_number': frame.edit_number
    }


def filter_frame_data(frame: MemoryFrame, filter_options: Dict[str, Any]) -> Dict:
    filtered_frame = {}

    if filter_options.get('type') == 'all':
        filtered_frame = frame.__dict__
    elif filter_options.get('type') == 'summary':
        filtered_frame = {
            'input': frame.input,
            'response1': frame.response1,
            'response2': frame.response2,
            'memory_data': frame.memory_data,
            'timestamp': frame.timestamp,
            'edit_number': frame.edit_number
        }
    elif filter_options.get('type') == 'specific_fields':
        fields = filter_options.get('fields', [])
        filtered_frame = {k: v for k, v in frame.__dict__.items() if k in fields}
        if 'memory_data' in fields:
            filtered_frame['memory_data'] = frame.memory_data
    else:
        raise ValueError(f"Unknown filter_type: {filter_options.get('type')}")

    if filter_options.get('included_only_filled_areas', False):
        filtered_frame = {k: v for k, v in filtered_frame.items() if v}
        if 'memory_data' in filtered_frame:
            filtered_frame['memory_data'] = {k: v for k, v in filtered_frame['memory_data'].items() if v}

    nested_filter = filter_options.get('nested_filter')
    if nested_filter and 'memory_data' in filtered_frame:
        filtered_frame['memory_data'] = apply_nested_filter(filtered_frame['memory_data'], nested_filter)

    return filtered_frame


def apply_nested_filter(data: Dict, filter_options: Dict) -> Dict:
    filtered_data = {}

    if filter_options.get('type') == 'all':
        filtered_data = data
    elif filter_options.get('type') == 'specific_fields':
        fields = filter_options.get('fields', [])
        filtered_data = {k: v for k, v in data.items() if k in fields}
    elif filter_options.get('type') == 'regex':
        regex_pattern = filter_options.get('regex', '')
        filtered_data = {k: v for k, v in data.items() if re.match(regex_pattern, k)}
    else:
        raise ValueError(f"Unknown nested filter type: {filter_options.get('type')}")

    return filtered_data


def RETRIVE_RELEVANT_FRAMES(query: str) -> List[Dict[str, Any]]:
    pretty_print("Starting retrieval process...", SEARCH)
    memory_frames = load_memory_frames(MEMORY_FRAMES_DIR)
    # Generate embeddings for all frames
    embeddings = generate_memory_embeddings(memory_frames)

    # Check number of frames and embeddings
    num_frames = len(memory_frames)
    num_embeddings = len(embeddings)

    if num_frames > num_embeddings:
        # Add additional embeddings
        pretty_print(f"Adding embeddings for {num_frames - num_embeddings} new frames...", BRAIN)
        for frame in memory_frames:
            if frame.frame_name not in embeddings:
                embeddings[frame.frame_name] = frame.get_embedding()

        save_embeddings(embeddings)

    retrieved_frames = retrieve_relevant_memory_frames(
        query=query,
        retrieval_method='cosine_similarity',
        filter_type='summary',
        top_n=2,
        update_embeddings=True,  # Update embeddings during retrieval
        included_only_filled_areas=True,
        memory_frames=memory_frames
    )

    filter_options = {
        'type': 'specific_fields',
        'fields': ['memory_data'],
        'included_only_filled_areas': True,
        'nested_filter': {
            'type': 'specific_fields',
            'fields': ['type', 'summary', 'impact', 'importance', 'observations']
        }
    }

    frames_content = []
    for frame_data in retrieved_frames['relevant_frames']:
        frame = MemoryFrame(frame_data, frame_data.get('frame_name', 'Unknown'),
                            frame_data.get('frame_path', 'Unknown'))
        filtered_frame = filter_frame_data(frame, filter_options)
        print(json.dumps(filtered_frame, indent=2, cls=NumpyEncoder))
        frames_content.append(filtered_frame)

    pretty_print("Retrieval process completed", SUCCESS)
    return frames_content