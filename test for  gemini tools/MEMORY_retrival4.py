import os
import json
import re
from collections import defaultdict

import nltk
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
import spacy
from whoosh import index
from whoosh.fields import Schema, TEXT, ID, NUMERIC, KEYWORD
from whoosh.qparser import MultifieldParser, QueryParser
from whoosh.analysis import StandardAnalyzer
from fuzzywuzzy import fuzz, process
from colorama import Fore, Style

# Use SpaCy for word embeddings and similarity calculations
try:
    nlp = spacy.load("en_core_web_md")  # Use 'md' or 'lg' for word vectors
except OSError:
    os.system("python -m spacy download en_core_web_md")
    nlp = spacy.load("en_core_web_md")

nltk.download('stopwords', quiet=True)
nltk.download('punkt', quiet=True)

def create_schema():
    """Defines the schema for the Whoosh index."""
    print(f"{Fore.CYAN}--- Creating Schema ---{Style.RESET_ALL}")
    return Schema(
        filepath=ID(stored=True),
        creation_date=TEXT(stored=True),
        concise_summary=TEXT(stored=True),
        description=TEXT(analyzer=StandardAnalyzer(), stored=True),
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
        frame_name_keywords=KEYWORD(commas=True, scorable=True),
        linked_concepts=KEYWORD(commas=True, scorable=True)
    )


def load_connection_map(connection_map_path):
    """Loads the connection map from the specified file."""
    connection_map = defaultdict(list)
    print(f"{Fore.CYAN}--- Loading Connection Map ---{Style.RESET_ALL}")
    if os.path.exists(connection_map_path):
        with open(connection_map_path, 'r', encoding='utf-8') as file:
            content = file.read()
            folder_matches = re.findall(
                r'\*\*\*\*(.*?)\*\*\*\*(.*?)Path:\s*(.*?)\n',
                content,
                re.DOTALL
            )
            for match in folder_matches:
                folder_name, _, folder_path = match
                connection_map[folder_name.strip()].append(
                    folder_path.strip()
                )
                print(
                    f"{Fore.GREEN}Folder: {folder_name.strip()} => Path: "
                    f"{folder_path.strip()}{Style.RESET_ALL}"
                )
    return connection_map


def build_knowledge_graph(connection_map):
    """Builds a knowledge graph from the connection map."""
    print(f"{Fore.CYAN}--- Building Knowledge Graph ---{Style.RESET_ALL}")
    graph = {}
    for concept, paths in connection_map.items():
        graph[concept] = set()
        for path in paths:
            terms = path.split("/")
            for term in terms:
                graph[concept].add(term)
    return graph


def index_memory_frames(schema, index_dir, connection_map):
    """Indexes the memory frames from the 'memories' folder."""
    if not os.path.exists(index_dir):
        os.mkdir(index_dir)

    ix = index.create_in(index_dir, schema)
    writer = ix.writer()

    frames_indexed = 0
    print(f"{Fore.CYAN}--- Indexing Memory Frames ---{Style.RESET_ALL}")
    for root, _, files in os.walk("memories"):
        for file in files:
            if file.endswith(".json"):
                file_path = os.path.join(root, file)
                print(f"{Fore.GREEN}Indexing Frame: {file_path}{Style.RESET_ALL}")

                try:
                    with open(file_path, 'r', encoding='utf-8') as json_file:
                        frame_data = json.load(json_file)
                        memory_data = frame_data.get('memory_data', {})

                        importance_level = int(memory_data.get(
                            'importance', {}
                        ).get('importance_level', '0'))
                        strength_of_matching = int(memory_data.get(
                            'storage', {}
                        ).get('memory_folders_storage', [{
                            'probability': '0'
                        }])[0].get('probability', '0'))
                        folder_paths = ",".join(
                            f["folder_path"] for f in memory_data.get(
                                'storage', {}
                            ).get('memory_folders_storage', [])
                        )

                        memory_frame_name = memory_data.get(
                            'naming_suggestion', {}
                        ).get('memory_frame_name', 'N/A')
                        frame_name_keywords = extract_keywords_from_name(
                            memory_frame_name
                        )

                        entities = memory_data.get('content', {}).get(
                            'entities', []
                        )
                        entities_list = [
                            e if isinstance(e, str) else str(e)
                            for e in entities
                        ]

                        extracted_content = []

                        def extract_text(data):
                            """Recursively extracts text from the data."""
                            if isinstance(data, str):
                                extracted_content.append(data)
                            elif isinstance(data, list):
                                for item in data:
                                    extract_text(item)
                            elif isinstance(data, dict):
                                for key, value in data.items():
                                    extract_text(key)
                                    extract_text(value)

                        extract_text(frame_data)
                        all_content = " ".join(extracted_content)

                        knowledge_graph = build_knowledge_graph(
                            connection_map
                        )
                        linked_concepts = []
                        for concept, related_terms in knowledge_graph.items():
                            extracted_content = []
                            extract_text(frame_data)
                            if any(
                                term in related_terms
                                for term in extracted_content
                            ):
                                linked_concepts.append(concept)

                        writer.add_document(
                            filepath=file_path,
                            creation_date=memory_data.get(
                                'metadata', {}
                            ).get('creation_date', 'N/A'),
                            concise_summary=memory_data.get(
                                'summary', {}
                            ).get('concise_summary', 'N/A'),
                            description=all_content,
                            keywords=",".join(memory_data.get(
                                'content', {}
                            ).get('keywords', [])),
                            entities=",".join(entities_list),
                            main_topic=memory_data.get(
                                'core', {}
                            ).get('main_topic', ''),
                            input=frame_data.get('input', ''),
                            response1=frame_data.get('response1', ''),
                            response2=frame_data.get('response2', ''),
                            importance_level=importance_level,
                            strength_of_matching=strength_of_matching,
                            storage_method=memory_data.get(
                                'storage', {}
                            ).get('storage_method', 'N/A'),
                            location=memory_data.get(
                                'storage', {}
                            ).get('location', 'N/A'),
                            memory_folders_storage=folder_paths,
                            memory_frame_name=memory_frame_name,
                            frame_name_keywords=",".join(
                                frame_name_keywords
                            ),
                            linked_concepts=",".join(linked_concepts)
                        )
                        frames_indexed += 1
                except json.JSONDecodeError as e:
                    print(
                        f"{Fore.RED}Error decoding JSON file {file_path}: {e}{Style.RESET_ALL}"
                    )

    writer.commit()
    print(f"\n{Fore.GREEN}Indexed {frames_indexed} memory frames.{Style.RESET_ALL}")
    return ix

def search_memory_frames(ix, query, knowledge_graph, fuzzy_threshold=80):
    """Searches the memory frames based on the given query."""
    print(f"{Fore.CYAN}--- Searching Memory Frames ---{Style.RESET_ALL}")
    with ix.searcher() as searcher:
        try:
            parser = MultifieldParser(
                [
                    "description",
                    "input",
                    "response1",
                    "response2",
                    "linked_concepts"
                ],
                schema=ix.schema
            )
            processed_query = preprocess_text(query)

            fuzzy_terms = []
            for term in processed_query.split():
                combined_lexicon = set()
                for field in [
                    "description",
                    "input",
                    "response1",
                    "response2"
                ]:
                    combined_lexicon.update(searcher.lexicon(field))

                fuzzy_matches = process.extractBests(
                    term,
                    combined_lexicon,
                    scorer=fuzz.token_sort_ratio,
                    score_cutoff=fuzzy_threshold,
                    limit=3
                )
                fuzzy_terms.extend(
                    [match[0] for match in fuzzy_matches]
                )

            if fuzzy_terms:
                fuzzy_query = " OR ".join(
                    [str(term, 'utf-8') for term in fuzzy_terms]
                )
                parser = QueryParser("description", schema=ix.schema)
                fuzzy_q = parser.parse(fuzzy_query)
                processed_query = (
                    f"{processed_query} OR {fuzzy_q}"
                )

            # Calculate query embedding using SpaCy
            query_doc = nlp(processed_query)

            concept_similarities = {}
            for concept in knowledge_graph:
                try:
                    concept_doc = nlp(concept)
                    similarity = query_doc.similarity(concept_doc)
                    concept_similarities[concept] = similarity
                except Exception as e:
                    print(f"{Fore.RED}Error calculating similarity: {e}{Style.RESET_ALL}")
                    pass  

            sorted_concepts = sorted(
                concept_similarities,
                key=concept_similarities.get,
                reverse=True
            )

            latent_space_query = " OR ".join(
                [f'linked_concepts:"{concept}"'
                 for concept in sorted_concepts]
            )
            combined_query = (
                f"{processed_query} OR ({latent_space_query})"
            )

            myquery = parser.parse(combined_query)
            results = searcher.search(myquery, limit=None)

            # Modify the results (create copies)
            modified_results = []
            for result in results:
                modified_result = dict(result)  # Create a copy
                for field in [
                    "description",
                    "input",
                    "response1",
                    "response2"
                ]:
                    content = modified_result.get(field, '') 
                    for term in processed_query.split():
                        highlighted_content = re.sub(
                            rf"\b({re.escape(term)})\b",
                            rf"{Fore.RED}\1{Style.RESET_ALL}",
                            content,
                            flags=re.IGNORECASE
                        )
                        modified_result[field] = highlighted_content
                modified_results.append(modified_result) 

            return modified_results 

        except Exception as e:
            print(f"{Fore.RED}An error occurred during search: {e}{Style.RESET_ALL}")
            return []


def preprocess_text(text):
    """Preprocesses the text for searching."""
    print(f"{Fore.CYAN}--- Preprocessing Text ---{Style.RESET_ALL}")
    stemmer = PorterStemmer()
    stop_words = set(stopwords.words('english'))
    words = nltk.word_tokenize(text)
    processed_words = [
        stemmer.stem(word.lower())
        if word.lower() not in ["deep learning"]
        else word.lower()
        for word in words
        if word.lower() not in stop_words
    ]
    return " ".join(processed_words)


def retrieve_contextual_frames(
    memory_frames,
    main_frame_index,
    num_frames_before=1,
    num_frames_after=1
):
    """Retrieves contextual frames around a given frame."""
    print(f"{Fore.CYAN}--- Retrieving Contextual Frames ---{Style.RESET_ALL}")
    selected_frames = []
    start_index = max(0, main_frame_index - num_frames_before)
    end_index = min(
        len(memory_frames), main_frame_index + num_frames_after + 1
    )
    selected_frames.extend(memory_frames[start_index:end_index])
    return selected_frames


def find_similar_folders(connection_map, query, threshold=80):
    """Finds similar folders based on the query."""
    print(f"{Fore.CYAN}--- Finding Similar Folders ---{Style.RESET_ALL}")
    similar_folders = {}
    for folder_name, folder_paths in connection_map.items():
        similarity_score = fuzz.token_sort_ratio(folder_name, query)
        if similarity_score >= threshold:
            similar_folders[folder_name] = folder_paths
    return similar_folders


def retrieve_by_importance(memory_frames, threshold=50):
    """Retrieves frames based on importance level."""
    print(f"{Fore.CYAN}--- Retrieving by Importance ---{Style.RESET_ALL}")
    return [
        frame
        for frame in memory_frames
        if frame.get('importance_level', 0) >= threshold
    ]


def retrieve_by_strength(memory_frames, threshold=50):
    """Retrieves frames based on strength of matching."""
    print(f"{Fore.CYAN}--- Retrieving by Strength ---{Style.RESET_ALL}")
    return [
        frame
        for frame in memory_frames
        if frame.get('strength_of_matching', 0) >= threshold
    ]


def retrieve_by_folder_match(connection_map, query, threshold=80):
    """Retrieves frames based on folder matching."""
    print(f"{Fore.CYAN}--- Retrieving by Folder Match ---{Style.RESET_ALL}")
    return find_similar_folders(connection_map, query, threshold)


def analyze_query_in_context(connection_map, query):
    """Analyzes the query in the context of the connection map."""
    print(f"{Fore.CYAN}--- Analyzing Query in Context ---{Style.RESET_ALL}")
    matching_folders = find_similar_folders(connection_map, query)

    if matching_folders:
        print(f"{Fore.GREEN}Query '{query}' found in the following categories:{Style.RESET_ALL}")
        for folder_name, paths in matching_folders.items():
            print(f"{Fore.BLUE}  Category: {folder_name}{Style.RESET_ALL}")
            print(f"{Fore.BLUE}    Paths: {paths}{Style.RESET_ALL}")
    else:
        print(f"{Fore.RED}Query '{query}' not found in any specific category.{Style.RESET_ALL}")


def extract_keywords_from_name(frame_name):
    """Extracts keywords from the frame name using spaCy."""
    print(f"{Fore.CYAN}--- Extracting Keywords from Name ---{Style.RESET_ALL}")
    doc = nlp(frame_name)
    keywords = [
        token.text
        for token in doc
        if token.pos_ in {"NOUN", "PROPN", "ADJ"}
    ]
    return keywords


def path_based_retrieval(connection_map, query, threshold=80):
    """Performs path-based retrieval using fuzzy matching."""
    print(f"{Fore.CYAN}--- Path-Based Retrieval ---{Style.RESET_ALL}")
    matching_paths = []

    for folder_name, folder_paths in connection_map.items():
        for path in folder_paths:
            path_terms = path.split('/')
            similarity_score = 0
            for term in path_terms:
                similarity_score += fuzz.token_sort_ratio(term, query)
            if similarity_score / len(path_terms) >= threshold:
                matching_paths.append(path)

    if matching_paths:
        print(f"{Fore.GREEN}Matching paths for '{query}':{Style.RESET_ALL}")
        for path in matching_paths:
            print(f"{Fore.BLUE}  {path}{Style.RESET_ALL}")
    else:
        print(f"{Fore.RED}No matching paths found for '{query}'.{Style.RESET_ALL}")

    return matching_paths


def process_retrieval(connection_map, ix, knowledge_graph):
    """Handles the memory retrieval process."""
    print(f"{Fore.CYAN}--- Memory Retrieval Process ---{Style.RESET_ALL}")
    while True:
        user_query = input("Enter your memory query: ")
        analyze_query_in_context(connection_map, user_query)
        print(f"{Fore.CYAN}--- Searching All Frames ---{Style.RESET_ALL}")

        with ix.searcher() as searcher:
            results = search_memory_frames(
                ix, user_query, knowledge_graph
            )

        if results:
            print(f"\n{Fore.GREEN}Retrieved {len(results)} memory frames:{Style.RESET_ALL}")
            results.sort(
                key=lambda x: x['strength_of_matching'],
                reverse=True
            )
            for i, frame in enumerate(results):
                folders_storage = frame['memory_folders_storage']
                print(f"{Fore.BLUE}{i+1}. Frame: {frame}{Style.RESET_ALL}")
                print(
                    f"   {Fore.GREEN}Folders: "
                    f"{folders_storage}{Style.RESET_ALL}"
                )
        else:
            print(f"{Fore.RED}No memory frames found matching the query.{Style.RESET_ALL}")

        matching_paths = path_based_retrieval(
            connection_map, user_query
        )

        if matching_paths:
            print(f"{Fore.CYAN}--- Searching Frames in Matching Paths ---{Style.RESET_ALL}")
            # Implement logic to search within matching paths

        if input("Continue searching? (y/n): ").lower() != 'y':
            break


def main():
    """Main function for memory retrieval system."""
    print(f"{Fore.CYAN}--- Memory Retrieval System ---{Style.RESET_ALL}")
    script_path = os.path.abspath(os.path.dirname(__file__))
    connection_map_path = os.path.join(
        script_path,
        "memories",
        "Memory_connections_map.txt"
    )
    index_dir = os.path.join(script_path, "memory_index")

    print(f"Current directory: {script_path}")
    print(f"Connection map path: {connection_map_path}")

    # Load the connection map
    connection_map = load_connection_map(connection_map_path)
    knowledge_graph = build_knowledge_graph(connection_map)

    # Create/load the Whoosh index
    if not os.path.exists(index_dir):
        print(f"Creating new index at: {index_dir}")
        os.mkdir(index_dir)
        schema = create_schema()
        ix = index.create_in(index_dir, schema)
        index_memory_frames(schema, index_dir, connection_map)
    else:
        print(f"Loading existing index from: {index_dir}")
        ix = index.open_dir(index_dir)

    try:
        process_retrieval(connection_map, ix, knowledge_graph)
    finally:
        ix.close()


if __name__ == "__main__":
    main()