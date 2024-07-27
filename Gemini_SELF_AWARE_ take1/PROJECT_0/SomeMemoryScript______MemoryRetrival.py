import json
import os
import torch
from transformers import BertTokenizer, BertModel
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
from termcolor import colored, cprint
from difflib import SequenceMatcher

# Directory where memory frames are stored
MEMORY_FRAMES_DIR = './memory'  # Adjust this path if needed
EMBEDDINGS_FILE = 'memory_embeddings.npy'  # File to store embeddings

# Load BERT model and tokenizer
tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')
model = BertModel.from_pretrained('bert-base-uncased')

# Function to load memory frames from directory, including subdirectories
def load_memory_frames(memory_frames_dir):
    cprint("Loading memory frames...", color="cyan")
    memory_frames = []
    seen_names = set()  # Keep track of processed file names
    for root, _, files in os.walk(memory_frames_dir):
        for file_name in files:
            if file_name.endswith('.json'):
                file_path = os.path.join(root, file_name)

                # Check if a similar frame has already been processed
                if is_similar_frame(file_name, seen_names):
                    cprint(f"Skipping similar frame: {file_path}", color="yellow")
                    continue

                try:
                    with open(file_path, 'r') as file:
                        memory_frame = json.load(file)
                        if validate_memory_frame(memory_frame):
                            memory_frames.append(memory_frame)
                            seen_names.add(file_name)  # Add file name to seen_names
                        else:
                            cprint(f"Skipping broken frame: {file_path}", color="yellow")
                except json.JSONDecodeError:
                    cprint(f"Skipping invalid JSON file: {file_path}", color="red")
    return memory_frames

# Function to validate a memory frame (checks for structure)
def validate_memory_frame(memory_frame):
    # Check for essential fields
    required_fields = [
        "input",
        "response1",
        "response2",
        "memory_data",
        "timestamp",
        "edit_number"
    ]
    for field in required_fields:
        if field not in memory_frame:
            return False

    # Check nested structures
    required_nested_fields = [
        "metadata",
        "type",
        "engine",
        "summary",
        "content",
        "interaction",
        "impact",
        "importance",
        "technical_details",
        "storage",
        "naming_suggestion"
    ]
    for field in required_nested_fields:
        if field not in memory_frame["memory_data"]:
            return False

    return True

# Function to get BERT embeddings for a given text
def get_bert_embedding(text):
    inputs = tokenizer(text, return_tensors='pt', truncation=True, padding=True)
    outputs = model(**inputs)
    cprint(f"Embedding for text: '{text}' - Shape: {outputs.last_hidden_state.mean(dim=1).detach().numpy().shape}",
           color="cyan")  # Print embedding details
    return outputs.last_hidden_state.mean(dim=1).detach().numpy()

# Function to generate embeddings for memory frames
def generate_memory_embeddings(memory_frames):
    cprint("Generating embeddings for memory frames...", color="cyan")
    embeddings = []
    for frame in memory_frames:
        # Embed key sections
        core_embedding = get_bert_embedding(" ".join(frame["memory_data"]["engine"].values()))
        summary_embedding = get_bert_embedding(frame["memory_data"]["summary"]["description"])
        content_embedding = get_bert_embedding(" ".join(frame["memory_data"]["content"]["keywords"]))

        # Combine section embeddings (using a weighted average)
        combined_embedding = (
                0.3 * core_embedding +
                0.4 * summary_embedding +
                0.3 * content_embedding
        )

        embeddings.append(combined_embedding.flatten())
        cprint(f"Frame embedding shape: {combined_embedding.flatten().shape}", color="cyan")  # Print embedding shape
    return np.stack(embeddings, axis=0)

# Function to filter and rank memory frames using embeddings
def retrieve_relevant_memory_frames(memory_frames, memory_embeddings, query):
    cprint("Retrieving relevant memory frames...", color="cyan")
    query_embedding = get_bert_embedding(query)
    query_embedding = query_embedding.reshape(1, -1)

    if len(memory_embeddings) == 0:
        cprint("No valid memory embeddings found.", color="red")
        return []

    similarities = cosine_similarity(query_embedding, memory_embeddings)[0]
    ranked_frames = sorted(zip(similarities, memory_frames), reverse=True, key=lambda x: x[0])
    cprint(f"Found {len(ranked_frames)} relevant frames.", color="green")
    return [frame for score, frame in ranked_frames[:5]]

# Function to check if two file names are similar
def is_similar_frame(file_name, seen_names):
    for seen_name in seen_names:
        # Check for differences of 1 character or 1 number
        if SequenceMatcher(None, file_name, seen_name).ratio() > 0.9:
            return True
    return False

# Main function
def main():
    # Load memory frames
    memory_frames = load_memory_frames(MEMORY_FRAMES_DIR)

    if not memory_frames:
        cprint("No valid memory frames to process. Exiting.", color="red")
        return

    # Check if embeddings file exists, otherwise generate and save them
    if os.path.exists(EMBEDDINGS_FILE):
        cprint("Loading pre-computed embeddings...", color="cyan")
        memory_embeddings = np.load(EMBEDDINGS_FILE)
    else:
        cprint("Generating embeddings and saving to file...", color="cyan")
        memory_embeddings = generate_memory_embeddings(memory_frames)
        np.save(EMBEDDINGS_FILE, memory_embeddings)

    if memory_embeddings.size == 0:
        cprint("No embeddings were generated. Exiting.", color="red")
        return

    # Example query
    query = input(colored("Enter your query:", "blue"))

    # Retrieve relevant memory frames
    relevant_frames = retrieve_relevant_memory_frames(memory_frames, memory_embeddings, query)

    # Print the most relevant frames
    if relevant_frames:
        cprint("Top 5 Relevant Frames:", color="green")
        for frame in relevant_frames:
            cprint(json.dumps(frame, indent=2), color="yellow")
    else:
        cprint("No relevant frames found for the query.", color="red")

if __name__ == "__main__":
    main()