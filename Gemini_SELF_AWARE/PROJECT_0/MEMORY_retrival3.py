import os
import json
import re
from whoosh import index
from whoosh.fields import Schema, TEXT, ID, NUMERIC, KEYWORD
from whoosh.qparser import MultifieldParser, QueryParser
from fuzzywuzzy import fuzz, process
from collections import defaultdict
import tempfile
import nltk
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
import spacy

# Check if the SpaCy model is downloaded, if not, download it.
try:
    nlp = spacy.load("en_core_web_sm")
except OSError:
    os.system("python -m spacy download en_core_web_sm")
    nlp = spacy.load("en_core_web_sm")

# Check if NLTK resources need to be downloaded
nltk.download('stopwords', quiet=True)
nltk.download('punkt', quiet=True)

# --- Schema Definition ---
def create_schema():
    return Schema(
        filepath=ID(stored=True),
        creation_date=TEXT(stored=True),
        concise_summary=TEXT(stored=True),
        description=TEXT(stored=True),
        keywords=KEYWORD(commas=True, scorable=True),
        entities=KEYWORD(commas=True, scorable=True),
        main_topic=TEXT(stored=True),
        input=TEXT(stored=True),
        response1=TEXT(stored=True),
        response2=TEXT(stored=True),
        importance_level=NUMERIC(stored=True),
        strength_of_matching=NUMERIC(stored=True),
        storage_method=TEXT(stored=True),
        location=TEXT(stored=True),
        memory_folders_storage=KEYWORD(commas=True, stored=True),
        memory_frame_name=TEXT(stored=True),
        frame_name_keywords=KEYWORD(commas=True, stored=True)
    )

# --- Connection Map Loading ---
def load_connection_map(connection_map_path):
    connection_map = defaultdict(list)
    print("\n--- Loading Connection Map ---")
    if os.path.exists(connection_map_path):
        with open(connection_map_path, 'r', encoding='utf-8') as file:
            content = file.read()
            folder_matches = re.findall(r'\*\*\*\*(.*?)\*\*\*\*(.*?)Path:\s*(.*?)\n', content, re.DOTALL)
            for match in folder_matches:
                folder_name, _, folder_path = match
                connection_map[folder_name.strip()].append(folder_path.strip())
                print(f"Folder: {folder_name.strip()} => Path: {folder_path.strip()}")
    return connection_map

# --- Memory Frame Indexing ---
def index_memory_frames(schema, index_dir):
    if not os.path.exists(index_dir):
        os.mkdir(index_dir)

    ix = index.create_in(index_dir, schema)
    writer = ix.writer()

    frames_indexed = 0
    print("\n--- Loading Memory Frames ---")
    for root, _, files in os.walk("memories"):
        for file in files:
            if file.endswith(".json"):
                file_path = os.path.join(root, file)
                print(f"Loaded Frame: {file_path}")

                try:
                    with open(file_path, 'r', encoding='utf-8') as json_file:
                        frame_data = json.load(json_file)
                        memory_data = frame_data.get('memory_data', {})

                        importance_level = int(memory_data.get('importance', {}).get('importance_level', '0'))
                        strength_of_matching = int(memory_data.get('storage', {}).get('memory_folders_storage', [{'probability': '0'}])[0].get('probability', '0'))

                        folder_paths = ",".join(f["folder_path"] for f in memory_data.get('storage', {}).get('memory_folders_storage', []))

                        # Extract keywords from frame name
                        memory_frame_name = memory_data.get('naming_suggestion', {}).get('memory_frame_name', 'N/A')
                        frame_name_keywords = extract_keywords_from_name(memory_frame_name)

                        # Parsing entities (assuming they should be strings)
                        entities = memory_data.get('content', {}).get('entities', [])
                        entities_list = [e if isinstance(e, str) else str(e) for e in entities]

                        writer.add_document(
                            filepath=file_path,
                            creation_date=memory_data.get('metadata', {}).get('creation_date', 'N/A'),
                            concise_summary=memory_data.get('summary', {}).get('concise_summary', 'N/A'),
                            description=memory_data.get('summary', {}).get('description', ''),
                            keywords=",".join(memory_data.get('content', {}).get('keywords', [])),
                            entities=",".join(entities_list),
                            main_topic=memory_data.get('core', {}).get('main_topic', ''),
                            input=frame_data.get('input', ''),
                            response1=frame_data.get('response1', ''),
                            response2=frame_data.get('response2', ''),
                            importance_level=importance_level,
                            strength_of_matching=strength_of_matching,
                            storage_method=memory_data.get('storage', {}).get('storage_method', 'N/A'),
                            location=memory_data.get('storage', {}).get('location', 'N/A'),
                            memory_folders_storage=folder_paths,
                            memory_frame_name=memory_frame_name,
                            frame_name_keywords=",".join(frame_name_keywords)
                        )
                        frames_indexed += 1
                except json.JSONDecodeError as e:
                    print(f"Error decoding JSON file {file_path}: {e}")

    writer.commit()
    print(f"\nIndexed {frames_indexed} memory frames.")
    return ix

# --- Memory Frame Searching ---
def search_memory_frames(ix, query, fuzzy_threshold=80):
    with ix.searcher() as searcher:
        try:
            parser = MultifieldParser(
                ["creation_date", "concise_summary", "description", "keywords", "entities", "main_topic", "input",
                 "response1", "response2", "storage_method", "location", "memory_folders_storage",
                 "memory_frame_name", "frame_name_keywords"],
                schema=ix.schema
            )

            processed_query = preprocess_text(query)

            # Fuzzy Matching
            fuzzy_terms = []
            for term in processed_query.split():
                fuzzy_matches = process.extractBests(term, searcher.lexicon("description"),
                                                     scorer=fuzz.token_sort_ratio, score_cutoff=fuzzy_threshold, limit=3)
                fuzzy_terms.extend([match[0] for match in fuzzy_matches])

            if fuzzy_terms:
                # Convert fuzzy_terms to strings before joining
                fuzzy_query = " OR ".join([str(term, 'utf-8') for term in fuzzy_terms])
                parser = QueryParser("description", schema=ix.schema)  # Use QueryParser
                fuzzy_q = parser.parse(fuzzy_query)
                processed_query = f"{processed_query} OR {fuzzy_q}"

            myquery = parser.parse(processed_query)
            results = searcher.search(myquery, limit=None)
            return [dict(hit) for hit in results]
        finally:
            searcher.close()

# --- Text Preprocessing ---
def preprocess_text(text):
    stemmer = PorterStemmer()
    stop_words = set(stopwords.words('english'))
    words = nltk.word_tokenize(text)
    processed_words = [stemmer.stem(word.lower()) for word in words if word.lower() not in stop_words]
    return " ".join(processed_words)

# --- Contextual Frame Retrieval ---
def retrieve_contextual_frames(memory_frames, main_frame_index, num_frames_before=1, num_frames_after=1):
    selected_frames = []
    start_index = max(0, main_frame_index - num_frames_before)
    end_index = min(len(memory_frames), main_frame_index + num_frames_after + 1)
    selected_frames.extend(memory_frames[start_index:end_index])
    return selected_frames

# --- Similar Folder Finding ---
def find_similar_folders(connection_map, query, threshold=80):
    similar_folders = {}
    for folder_name, folder_paths in connection_map.items():
        similarity_score = fuzz.token_sort_ratio(folder_name, query)
        if similarity_score >= threshold:
            similar_folders[folder_name] = folder_paths
    return similar_folders

# --- Memory Retrieval Strategies ---
def retrieve_by_importance(memory_frames, threshold=50):
    return [frame for frame in memory_frames if frame.get('importance_level', 0) >= threshold]

def retrieve_by_strength(memory_frames, threshold=50):
    return [frame for frame in memory_frames if frame.get('strength_of_matching', 0) >= threshold]

def retrieve_by_folder_match(connection_map, query, threshold=80):
    return find_similar_folders(connection_map, query, threshold)

# --- Query Context Analysis ---
def analyze_query_in_context(connection_map, query):
    print("\n--- Analyzing Query in Context ---")
    matching_folders = find_similar_folders(connection_map, query)

    if matching_folders:
        print(f"Query '{query}' found in the following categories:")
        for folder_name, paths in matching_folders.items():
            print(f"  Category: {folder_name}")
            print(f"    Paths: {paths}")
    else:
        print(f"Query '{query}' not found in any specific category.")

# --- Keyword Extraction from Frame Name ---
def extract_keywords_from_name(frame_name):
    doc = nlp(frame_name)
    keywords = [token.text for token in doc if token.pos_ in {"NOUN", "PROPN", "ADJ"}]
    return keywords

# --- Main Retrieval Process ---
def process_retrieval(connection_map, ix):
    while True:
        user_query = input("Enter your memory query: ")

        analyze_query_in_context(connection_map, user_query)

        print("\n--- Searching All Frames ---")

        # Create a new searcher for each search
        with ix.searcher() as searcher:
            results = search_memory_frames(ix, user_query)

        if results:
            print(f"\nRetrieved {len(results)} memory frames:")
            for i, frame in enumerate(results):
             print(f"{i}  frame {frame}")
        else:
            print("No memory frames found matching the query.")

        if input("Continue searching? (y/n): ").lower() != 'y':
            break
# --- Main Function ---
def main():
    script_path = os.path.abspath(os.path.dirname(__file__))
    connection_map_path = os.path.join(script_path, "memories", "Memory_connections_map.txt")
    index_dir = os.path.join(script_path, "memory_index")  # Directory for the index

    print("\n--- Memory Retrieval System ---")
    print(f"Current directory: {script_path}")
    print(f"Connection map path: {connection_map_path}")

    connection_map = load_connection_map(connection_map_path)

    # Create the index if it doesn't exist
    if not os.path.exists(index_dir):
        os.mkdir(index_dir)
        schema = create_schema()
        ix = index.create_in(index_dir, schema)
        index_memory_frames(schema, index_dir)
    else:
        # Load existing index
        ix = index.open_dir(index_dir)

    # No need for temp_dir anymore

    # Now you can use the index for searching
    try:
        process_retrieval(connection_map, ix)
    finally:
        ix.close() # Always close the index when you are done with it.

if __name__ == "__main__":
    main()