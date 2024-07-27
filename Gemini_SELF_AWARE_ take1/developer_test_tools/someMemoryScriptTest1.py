import json
import os
import torch
from transformers import BertTokenizer, BertModel
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
from termcolor import colored, cprint

# Directory where memory frames are stored
MEMORY_FRAMES_DIR = './memory'  # Adjust this path if needed

# Load BERT model and tokenizer
tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')
model = BertModel.from_pretrained('bert-base-uncased')

# Function to load memory frames from directory, including subdirectories
def load_memory_frames(memory_frames_dir):
    cprint("Loading memory frames...", color="cyan")
    memory_frames = []
    for root, _, files in os.walk(memory_frames_dir):

        for file_name in files:
            print(file_name)
            if file_name.endswith('.json'):
                file_path = os.path.join(root, file_name)
                try:
                    with open(file_path, 'r') as file:
                        memory_frame = json.load(file)
                        print(f"validation..of. {file_name}")
                        if validate_memory_frame(memory_frame):
                            memory_frames.append(memory_frame)
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
    return outputs.last_hidden_state.mean(dim=1).detach().numpy()

# Function to generate embeddings for memory frames
def generate_memory_embeddings(memory_frames):
    cprint("Generating embeddings for memory frames...", color="cyan")
    embeddings = []
    for frame in memory_frames:
        print(frame)
        description = frame["memory_data"]["summary"]["description"]
        embedding = get_bert_embedding(description)
        embeddings.append(embedding.flatten()) # Flatten the embedding
    return np.stack(embeddings, axis=0)  # Create a 2D array

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
# Main function
def main():
    # Load memory frames
    memory_frames = load_memory_frames(MEMORY_FRAMES_DIR)

    if not memory_frames:
        cprint("No valid memory frames to process. Exiting.", color="red")
        return

    # Generate embeddings for memory frames
    memory_embeddings = generate_memory_embeddings(memory_frames)

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