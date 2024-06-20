import json
import os
import torch
from transformers import BertTokenizer, BertModel
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
from difflib import SequenceMatcher
from typing import List, Dict, Tuple
import logging
import uuid
import json
import numpy as np


# Enhanced Logging
logging.basicConfig(filename='memory_retrieval.log', level=logging.ERROR,
                    format='%(asctime)s - %(levelname)s - %(message)s')

# Memory Configuration
MEMORY_FRAMES_DIR = './memories'
EMBEDDINGS_FILE = 'memory_embeddings.npy'

# ANSI Color Codes
GREEN = "\033[92m"
YELLOW = "\033[93m"
BLUE = "\033[94m"
MAGENTA = "\033[95m"
CYAN = "\033[96m"
RED = "\033[91m"
ENDC = "\033[0m"  # To reset coloring

# Load BERT Model
print(f"{BLUE}🚀 Loading the mighty BERT model! This might take a moment... 🚀{ENDC}")
tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')
model = BertModel.from_pretrained('bert-base-uncased')
print(f"{GREEN}✅ BERT model loaded and ready for action! ✅{ENDC}")


def levenshtein_distance(s1: str, s2: str) -> int:
    """Calculates the Levenshtein distance between two strings."""
    if len(s1) > len(s2):
        s1, s2 = s2, s1
    distances = range(len(s1) + 1)
    for i2, c2 in enumerate(s2):
        new_distances = [i2 + 1]
        for i1, c1 in enumerate(s1):
            if c1 == c2:
                new_distances.append(distances[i1])
            else:
                new_distances.append(1 + min((distances[i1], distances[i1 + 1], new_distances[-1])))
        distances = new_distances
    return distances[-1]


def is_similar_frame(file_name: str, seen_names: set, threshold: float = 0.8) -> bool:
    """Checks if a file name is similar to already loaded frames."""
    for seen_name in seen_names:
        distance = levenshtein_distance(file_name.lower(), seen_name.lower())
        similarity = 1 - (distance / max(len(file_name), len(seen_name)))
        if similarity > threshold:
            print(f"{YELLOW}  ➡️ Similar frame detected: '{file_name}'. Skipping to avoid redundancy.{ENDC}")
            return True
    return False


def load_memory_frames(memory_frames_dir: str) -> List[Dict]:
    """
    Loads memory frames from JSON files.
    Generates a unique ID for frames missing an 'id'.
    """
    print(f"{CYAN}🧠 Loading Memory Frames...{ENDC}")
    memory_frames = []
    seen_names = set()
    for root, _, files in os.walk(memory_frames_dir):
        for file_name in files:
            if file_name.endswith('.json'):
                file_path = os.path.join(root, file_name)

                # Check for Similar Frames
                if is_similar_frame(file_name, seen_names):
                    continue

                try:
                    with open(file_path, 'r') as file:
                        memory_frame = json.load(file)

                        # Ensure Unique ID
                        if 'id' not in memory_frame:
                            memory_frame['id'] = str(uuid.uuid4())
                            print(f"{CYAN}  ✨ Generated ID for frame: {file_name}{ENDC}")

                        memory_frames.append(memory_frame)
                        seen_names.add(file_name)
                        print(f"{GREEN}  ✅ Loaded: '{file_name}'{ENDC}")
                except json.JSONDecodeError as e:
                    error_msg = f"{RED}  ❌ Invalid JSON in '{file_path}': {e}{ENDC}"
                    logging.error(error_msg)
                    print(error_msg)

    print(f"{MAGENTA}\n🧠 Loaded a total of {len(memory_frames)} memory frames! 🧠\n{ENDC}")
    memory_frams_str = str(memory_frames)
    print("MemoryFramesStrReturn:")
    print(f"{GREEN}{memory_frams_str}")

    return  memory_frams_str


def get_bert_embedding(text: str) -> np.ndarray:
    """Generates a BERT embedding (numerical representation) for a text."""
    try:
        inputs = tokenizer(text, return_tensors='pt', truncation=True, padding=True)
        with torch.no_grad():
            outputs = model(**inputs)
        embedding = outputs.last_hidden_state.mean(dim=1).detach().numpy()
        return embedding
    except Exception as e:
        error_msg = f"{RED}  ❌ Error generating embedding: {e}{ENDC}"
        logging.error(error_msg)
        print(error_msg)
        return np.zeros(768)


def generate_memory_embeddings(memory_frames: List[Dict],
                               key_fields: Tuple[str, ...] = ("input", "response1",
                                                              "memory_data")) -> Dict[str, np.ndarray]:
    """Generates and stores embeddings for each memory frame."""
    print(f"\n{BLUE}🤖 Generating Embeddings for Memory Frames... 🤖{ENDC}\n")
    embeddings = {}
    for frame in memory_frames:
        section_embeddings = []
        for field in key_fields:
            if field in frame:
                text = " ".join(str(value) for value in frame[field].values()) \
                    if isinstance(frame[field], dict) else str(frame[field])
                section_embeddings.append(get_bert_embedding(text))

        if section_embeddings:
            combined_embedding = np.mean(section_embeddings, axis=0)
            embeddings[frame['id']] = combined_embedding.flatten()
        else:
            warning_msg = f"{YELLOW}  ⚠️ No key fields found in frame: {frame['id']}. Skipping embedding generation.{ENDC}"
            logging.warning(warning_msg)
            print(warning_msg)
    print(f"\n{GREEN}🤖 Embeddings Generation Complete! 🤖{ENDC}\n")
    return embeddings


def retrieve_relevant_memory_frames(memory_frames: List[Dict],
                                    memory_embeddings: np.ndarray,
                                    query: str,
                                    top_n: int = 5) -> List[Tuple[float, Dict]]:
    """
    This function retrieves the most relevant memory frames related to
    a given query using cosine similarity.
    """
    print(f"\n{BLUE}🔍 Searching for Relevant Memories... 🔍{ENDC}\n")
    query_embedding = get_bert_embedding(query).reshape(1, -1)

    if len(memory_embeddings) == 0:
        print(f"{YELLOW}  ⚠️ No memory embeddings found!  ⚠️{ENDC}")
        return []

    similarities = cosine_similarity(query_embedding, memory_embeddings)[0]
    ranked_frames = sorted(zip(similarities, memory_frames), reverse=True, key=lambda x: x[0])

    print(f"{MAGENTA}✨ Found {len(ranked_frames)} relevant frames. ✨{ENDC}")
    return ranked_frames[:top_n]


def update_memory_embeddings(memory_embeddings: Dict[str, np.ndarray],
                             relevant_indices: List[int],
                             query_embedding: np.ndarray,
                             learning_rate: float = 0.01) -> Dict[str, np.ndarray]:
    """Fine-tunes the embeddings of relevant memories to be more similar
    to the query embedding, allowing the system to learn from new queries.
    """
    try:
        embedding_array = np.array(list(memory_embeddings.values()))
        for i in relevant_indices:
            embedding_array[i] = (1 - learning_rate) * embedding_array[i] + learning_rate * query_embedding
        updated_embeddings = dict(zip(memory_embeddings.keys(), embedding_array))
        print(f"{CYAN}🧠 Memory embeddings updated! 🧠{ENDC}")
        return updated_embeddings
    except Exception as e:
        error_msg = f"{RED}❌ Error updating memory embeddings: {e}{ENDC}"
        logging.error(error_msg)
        print(error_msg)
        return memory_embeddings


def RETRIEVE_RELEVANT_FRAMES_X(query: str) -> Dict:
    """
    Core function to retrieve relevant frames based on a query. It loads
    memory frames, computes embeddings if needed, performs the search, and
    returns the results with detailed information.
    """
    print(f"\n{BLUE}🚀 Processing Query: '{query}' 🚀\n{ENDC}")
    memory_frames = load_memory_frames(MEMORY_FRAMES_DIR)
    result_data = {
        "relevant_frames": [],
        "error": None
    }

    if not memory_frames:
        result_data["error"] = "No valid memory frames found."
        return result_data

    if os.path.exists(EMBEDDINGS_FILE):
        try:
            memory_embeddings = np.load(EMBEDDINGS_FILE, allow_pickle=True).item()
            print(f"{GREEN}  ✅ Loaded existing embeddings.{ENDC}")
        except Exception as e:
            logging.error(f"Error loading embeddings: {e}. Generating new embeddings.")
            print(f"{YELLOW}  ⚠️ Error loading embeddings: {e}. Generating new embeddings.{ENDC}")
            memory_embeddings = {}
    else:
        memory_embeddings = {}
        print(f"{YELLOW}  ➡️ No pre-computed embeddings found. Generating...{ENDC}")

    # Compute embeddings for new frames
    new_frames = False
    for frame in memory_frames:
        if frame['id'] not in memory_embeddings:
            print(f"{CYAN}  ➡️ Computing embedding for new frame: {frame['id']}{ENDC}")
            memory_embeddings.update(generate_memory_embeddings([frame]))
            new_frames = True

    # Save updated embeddings
    if new_frames:
        try:
            np.save(EMBEDDINGS_FILE, memory_embeddings)
            print(f"{GREEN}  ✅ Embeddings updated and saved.{ENDC}")
        except Exception as e:
            logging.error(f"Error saving embeddings: {e}")
            print(f"{RED}  ❌ Error saving embeddings: {e}{ENDC}")

    try:
        memory_embeddings_array = np.array(list(memory_embeddings.values()))
        ranked_frames = retrieve_relevant_memory_frames(
            memory_frames, memory_embeddings_array, query
        )

        if ranked_frames:
            for score, frame in ranked_frames:
                frame_data = {
                    "similarity_score": float(score),  # Add similarity score

                    "timestamp": frame.get("timestamp", ""),
                    "edit_number": frame.get("edit_number", 0),
                    "metadata": frame.get("metadata", {}),
                    "type": frame.get("type", ""),
                    "core": frame.get("core", {}),
                    "summary": frame.get("summary", {}),
                    "content": frame.get("content", {}),
                    "interaction": frame.get("interaction", {}),
                    "impact": frame.get("impact", {}),
                    "importance": frame.get("importance", {}),
                    "technical_details": frame.get("technical_details", {}),

                    # Access nested values in 'memory_data'
                    "memory_data_metadata": frame.get("memory_data", {}).get("metadata", {}),
                    "memory_data_type": frame.get("memory_data", {}).get("type", ""),
                    "memory_data_core": frame.get("memory_data", {}).get("core", {}),
                    "memory_data_summary": frame.get("memory_data", {}).get("summary", {}),
                    "memory_data_content": frame.get("memory_data", {}).get("content", {}),
                    "memory_data_interaction": frame.get("memory_data", {}).get("interaction", {}),
                    "memory_data_impact": frame.get("memory_data", {}).get("impact", {}),
                    "memory_data_importance": frame.get("memory_data", {}).get("importance", {}),
                    "memory_data_technical_details": frame.get("memory_data", {}).get("technical_details", {}),
                    "memory_data_storage": frame.get("memory_data", {}).get("storage", {}),
                    "memory_data_naming_suggestion": frame.get("memory_data", {}).get("naming_suggestion", {}),
                }
                result_data["relevant_frames"].append(frame_data)

            print(f"{MAGENTA}\n✨ Top Relevant Frames: ✨\n{ENDC}")
            for i, frame_data in enumerate(result_data["relevant_frames"]):
                print(f"{YELLOW}  🌟 Frame {i + 1} (Similarity: {frame_data['similarity_score']:.4f}):{ENDC}")
                print(json.dumps(frame_data, indent=4))
                print("-" * 30)

        else:
            result_data["error"] = "No relevant frames found for the query."
            print(f"{YELLOW}  😔 No relevant frames found for: '{query}' 😔{ENDC}")

    except Exception as e:
        logging.error(f"Error during embedding or retrieval: {e}")
        result_data["error"] = "An error occurred during processing."
        print(f"{RED}  ❌ An error occurred: {e}{ENDC}")

    return result_data


"""    """

def RETRIEVE_RELEVANT_FRAMES(query: str, Essentials="all") -> Dict:
    """
    Core function to retrieve relevant frames based on a query. It loads
    memory frames, computes embeddings if needed, performs the search, and
    returns the results with detailed information.
    """
    print(f"\n{BLUE}🚀 Processing Query: '{query}' 🚀\n{ENDC}")
    memory_frames = load_memory_frames(MEMORY_FRAMES_DIR)
    result_data = {
        "relevant_frames": [],
        "error": None
    }

    if not memory_frames:
        result_data["error"] = "No valid memory frames found."
        return result_data

    if os.path.exists(EMBEDDINGS_FILE):
        try:
            memory_embeddings = np.load(EMBEDDINGS_FILE, allow_pickle=True).item()
            print(f"{GREEN}  ✅ Loaded existing embeddings.{ENDC}")
        except Exception as e:
            logging.error(f"Error loading embeddings: {e}. Generating new embeddings.")
            print(f"{YELLOW}  ⚠️ Error loading embeddings: {e}. Generating new embeddings.{ENDC}")
            memory_embeddings = {}
    else:
        memory_embeddings = {}
        print(f"{YELLOW}  ➡️ No pre-computed embeddings found. Generating...{ENDC}")

    # Compute embeddings for new frames
    new_frames = False
    for frame in memory_frames:
        if frame['id'] not in memory_embeddings:
            print(f"{CYAN}  ➡️ Computing embedding for new frame: {frame['id']}{ENDC}")
            memory_embeddings.update(generate_memory_embeddings([frame]))
            new_frames = True

    # Save updated embeddings
    if new_frames:
        try:
            np.save(EMBEDDINGS_FILE, memory_embeddings)
            print(f"{GREEN}  ✅ Embeddings updated and saved.{ENDC}")
        except Exception as e:
            logging.error(f"Error saving embeddings: {e}")
            print(f"{RED}  ❌ Error saving embeddings: {e}{ENDC}")

    try:
        memory_embeddings_array = np.array(list(memory_embeddings.values()))
        ranked_frames = retrieve_relevant_memory_frames(
            memory_frames, memory_embeddings_array, query
        )

        if ranked_frames:
            for score, frame in ranked_frames:
                frame_data = {
                    "similarity_score": float(score),  # Add similarity score

                    "timestamp": frame.get("timestamp", ""),
                    "edit_number": frame.get("edit_number", 0),
                    "metadata": frame.get("metadata", {}),
                    "type": frame.get("type", ""),
                    "core": frame.get("core", {}),
                    "summary": frame.get("summary", {}),
                    "content": frame.get("content", {}),
                    "interaction": frame.get("interaction", {}),
                    "impact": frame.get("impact", {}),
                    "importance": frame.get("importance", {}),
                    "technical_details": frame.get("technical_details", {}),

                    # Access nested values in 'memory_data'
                    "memory_data_metadata": frame.get("memory_data", {}).get("metadata", {}),
                    "memory_data_type": frame.get("memory_data", {}).get("type", ""),
                    "memory_data_core": frame.get("memory_data", {}).get("core", {}),
                    "memory_data_summary": frame.get("memory_data", {}).get("summary", {}),
                    "memory_data_content": frame.get("memory_data", {}).get("content", {}),
                    "memory_data_interaction": frame.get("memory_data", {}).get("interaction", {}),
                    "memory_data_impact": frame.get("memory_data", {}).get("impact", {}),
                    "memory_data_importance": frame.get("memory_data", {}).get("importance", {}),
                    "memory_data_technical_details": frame.get("memory_data", {}).get("technical_details", {}),
                    "memory_data_storage": frame.get("memory_data", {}).get("storage", {}),
                    "memory_data_naming_suggestion": frame.get("memory_data", {}).get("naming_suggestion", {}),
                }
                result_data["relevant_frames"].append(frame_data)

            print(f"{MAGENTA}\n✨ Top Relevant Frames: ✨\n{ENDC}")
            for i, frame_data in enumerate(result_data["relevant_frames"]):
                print(f"{YELLOW}  🌟 Frame {i + 1} (Similarity: {frame_data['similarity_score']:.4f}):{ENDC}")
                print(json.dumps(frame_data, indent=4))
                print("-" * 30)

        else:
            result_data["error"] = "No relevant frames found for the query."
            print(f"{YELLOW}  😔 No relevant frames found for: '{query}' 😔{ENDC}")

    except Exception as e:
        logging.error(f"Error during embedding or retrieval: {e}")
        result_data["error"] = "An error occurred during processing."
        print(f"{RED}  ❌ An error occurred: {e}{ENDC}")

    if Essentials == "all":
        return_data = {
            "relevant_frames": [
                {
                    "similarity_score": frame_data["similarity_score"],
                    "memory_data": frame_data["memory_data"]
                }
                for frame_data in result_data["relevant_frames"]
            ]
        }
    elif Essentials == "sumarisation":
        return_data = {
            "relevant_frames": [
                {
                    "similarity_score": frame_data["similarity_score"],
                    "memory_data": {
                        "metadata": frame_data["memory_data_metadata"],
                        "type": frame_data["memory_data_type"],
                        "core": frame_data["memory_data_core"],
                        "summary": frame_data["memory_data_summary"],
                        "content": frame_data["memory_data_content"],
                        "interaction": frame_data["memory_data_interaction"],
                        "impact": frame_data["memory_data_impact"],
                        "importance": frame_data["memory_data_importance"],
                        "technical_details": frame_data["memory_data_technical_details"],


                    }
                }
                for frame_data in result_data["relevant_frames"]
            ]
        }
    elif Essentials == "sumarisation_OnlyExistingEntries":
        return_data = {
            "relevant_frames": [
                {
                    "similarity_score": frame_data["similarity_score"],
                    "memory_data": {
                        key: value for key, value in frame_data["memory_data"].items()
                        if value is not None and value != "" and value != []
                    }
                }
                for frame_data in result_data["relevant_frames"]
            ]
        }
    else:
        return_data = {
            "relevant_frames": [
                {
                    "similarity_score": frame_data["similarity_score"],
                    "memory_data": frame_data["memory_data"]
                }
                for frame_data in result_data["relevant_frames"]
            ]
        }

    print(f"\n{GREEN}  ✅ Returning: \n{ENDC}{json.dumps(return_data, indent=4)}")
    return return_data

"""   
# Example usage:
RETRIEVE_RELEVANT_FRAMES(query="What is deep learning?",Essentials="sumarisation")

"""