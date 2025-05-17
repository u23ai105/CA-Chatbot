import os
import json
import sqlite3
import faiss
import numpy as np
import spacy
import multiprocessing
from collections import OrderedDict
from textblob import TextBlob
from sentence_transformers import SentenceTransformer
from nltk.tokenize import sent_tokenize
from datetime import datetime
from concurrent.futures import ProcessPoolExecutor

# Load Spacy NLP model
nlp = spacy.load("en_core_web_sm")
nlp.max_length = 2_000_000

# Load Sentence Transformer model
embedding_model = SentenceTransformer('all-MiniLM-L6-v2')


# === Step 1: Advanced Data Cleaning ===
def advanced_cleaning(text):
    """Performs spell-check, deduplication, and lemmatization."""
    doc = nlp(text)
    corrected_text = str(TextBlob(text).correct())  # Spell check
    deduplicated_text = " ".join(OrderedDict.fromkeys(corrected_text.split()))  # Remove duplicate words
    lemmatized_text = " ".join([token.lemma_ for token in doc if not token.is_stop])  # Lemmatization
    return lemmatized_text


def process_batch(input_files, output_folder):
    """Processes a batch of 5 files at a time to prevent RAM overload."""
    os.makedirs(output_folder, exist_ok=True)

    for file_path in input_files:
        file_name = os.path.basename(file_path)
        output_path = os.path.join(output_folder, f"cleaned_{file_name}")

        with open(file_path, "r", encoding="utf-8") as f:
            raw_text = f.read()

        cleaned_text = advanced_cleaning(raw_text)

        with open(output_path, "w", encoding="utf-8") as f:
            f.write(cleaned_text)

        print(f"✅ Cleaned: {file_name}")


def clean_files_in_batches(input_folder, output_folder, batch_size=5):
    """Splits files into batches of 5 and processes them sequentially."""
    all_files = [os.path.join(input_folder, f) for f in os.listdir(input_folder) if f.endswith(".txt")]

    for i in range(0, len(all_files), batch_size):
        batch = all_files[i:i + batch_size]
        print(f"\n🚀 Processing batch {i // batch_size + 1}/{-(-len(all_files) // batch_size)} ({len(batch)} files)...")
        process_batch(batch, output_folder)


# === Step 2: Metadata Generation (Parallelized) ===
def process_file_for_metadata(file_path, category):
    """Extracts metadata such as keywords and entities from text files."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
    except Exception as e:
        print(f"❌ Error reading {file_path}: {e}")
        return None

    title = os.path.splitext(os.path.basename(file_path))[0]
    last_updated = datetime.now().strftime("%Y-%m-%d")
    entities, keywords = set(), set()

    doc = nlp(content)
    entities.update([ent.text for ent in doc.ents])
    keywords.update(content.lower().split()[:15])

    return (title, category, json.dumps(list(keywords)), json.dumps(list(entities)), last_updated)


def generate_metadata(folder_path, db_file="metadata.db", json_file="metadata.json"):
    """Creates a metadata database and stores extracted data."""
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS metadata (
                        title TEXT, category TEXT, keywords TEXT, entities TEXT, last_updated TEXT)''')

    metadata = []

    for root, _, files in os.walk(folder_path):
        category = os.path.basename(root)
        for file in files:
            if file.endswith(".txt"):
                file_path = os.path.join(root, file)
                result = process_file_for_metadata(file_path, category)
                if result:
                    cursor.execute("INSERT INTO metadata VALUES (?, ?, ?, ?, ?)", result)
                    metadata.append({
                        "title": result[0],
                        "category": result[1],
                        "keywords": json.loads(result[2]),
                        "entities": json.loads(result[3]),
                        "last_updated": result[4]
                    })

    conn.commit()
    conn.close()

    with open(json_file, "w", encoding="utf-8") as f:
        json.dump(metadata, f, indent=4)

    print(f"✅ Metadata stored in {db_file} (SQLite) and {json_file} (JSON)!")


# === Step 3: Smart Content Chunking ===
def chunk_text(text, max_sentences=5):
    """Splits text into chunks of 5 sentences each."""
    sentences = sent_tokenize(text)
    chunks = [" ".join(sentences[i:i + max_sentences]) for i in range(0, len(sentences), max_sentences)]
    return chunks


def save_chunks(input_folder, output_folder):
    """Splits large text files into smaller chunks for better indexing."""
    os.makedirs(output_folder, exist_ok=True)

    for root, _, files in os.walk(input_folder):
        for file in files:
            if file.endswith(".txt"):
                file_path = os.path.join(root, file)
                try:
                    with open(file_path, "r", encoding="utf-8") as f:
                        content = f.read()
                    chunks = chunk_text(content)
                    for idx, chunk in enumerate(chunks):
                        chunk_path = os.path.join(output_folder, f"chunk_{file}_{idx}.txt")
                        with open(chunk_path, "w", encoding="utf-8") as f:
                            f.write(chunk)
                except Exception as e:
                    print(f"❌ Error processing {file_path}: {e}")

    print(f"✅ Chunking complete!")


# === Step 4: FAISS Indexing ===
def build_faiss_index(documents, index_file):
    """Creates a FAISS index for efficient text retrieval."""
    embeddings = embedding_model.encode(documents)
    dimension = embeddings.shape[1]
    index = faiss.IndexHNSWFlat(dimension, 32)
    index.add(np.array(embeddings).astype('float32'))

    faiss.write_index(index, index_file)
    print(f"✅ FAISS index built and saved as {index_file}!")


def prepare_documents(folder_path):
    """Prepares text data for FAISS indexing."""
    documents = []
    for root, _, files in os.walk(folder_path):
        for file in files:
            if file.endswith(".txt"):
                file_path = os.path.join(root, file)
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        documents.append(f.read())
                except Exception as e:
                    print(f"❌ Error reading {file_path}: {e}")
    print(f"✅ {len(documents)} documents prepared for indexing.")
    return documents


# === Step 5: Verification ===
def verify_process(db_file="metadata.db", json_file="metadata.json", index_file="tax_data.index"):
    """Verifies metadata and FAISS index."""
    print("\n🔍 **Verification Results**:")

    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM metadata LIMIT 5")
    metadata_samples = cursor.fetchall()
    conn.close()
    print(f"\n📄 Sample Metadata from DB:\n{metadata_samples}")

    with open(json_file, "r", encoding="utf-8") as f:
        metadata_json = json.load(f)
    print(f"\n📄 Sample Metadata from JSON:\n{metadata_json[:2]}")

    index = faiss.read_index(index_file)
    print(f"\n📌 FAISS Index contains {index.ntotal} vectors!")


# **Execution**
if __name__ == "__main__":
    RAW_FOLDER = "/Users/muzammilmohammad/Desktop/CA chatbot/extracted_data"
    CLEANED_FOLDER = "./Cleaned_Data"
    CHUNKED_FOLDER = "./Chunked_Data"
    INDEX_FILE = "tax_data.index"

    print("🚀 Starting Data Structuring Pipeline (Processing 5 Files at a Time)...")

    clean_files_in_batches(RAW_FOLDER, CLEANED_FOLDER, batch_size=5)
    generate_metadata(CLEANED_FOLDER)
    save_chunks(CLEANED_FOLDER, CHUNKED_FOLDER)
    documents = prepare_documents(CHUNKED_FOLDER)
    build_faiss_index(documents, INDEX_FILE)

    verify_process()

    print("\n✅ **Data structuring and verification complete!** 🎉")
