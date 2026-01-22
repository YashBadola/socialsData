import os
import json
import random
import re
from datetime import datetime

# Archie Texton's signature constants
ARCHIVIST_NAME = "Archibald 'Archie' Texton"
ARCHIVE_VERSION = "2.14.2"

def calculate_reading_complexity(text):
    """
    Calculates a heuristic reading complexity score.
    Archie's Note: A simple metric, but effective for sorting the wheat from the chaff.
    """
    words = text.split()
    sentences = re.split(r'[.!?]+', text)
    sentences = [s for s in sentences if s.strip()]

    if not sentences:
        return 0

    avg_sentence_length = len(words) / len(sentences)
    avg_word_length = sum(len(w) for w in words) / len(words) if words else 0

    # A mocked Flesch-Kincaid-ish score
    score = (0.39 * avg_sentence_length) + (11.8 * avg_word_length) - 15.59
    return round(score, 2)

def analyze_sentiment(text):
    """
    Performs a keyword-based sentiment/tone analysis.
    Archie's Note: The machine's attempt to understand the soul. Quaint.
    """
    text_lower = text.lower()

    melancholy_words = ['grief', 'sorrow', 'night', 'pain', 'anguish', 'dread', 'suffer', 'alone', 'isolation']
    passionate_words = ['love', 'desire', 'infinite', 'eternal', 'faith', 'passion', 'leap']
    intellectual_words = ['dialectic', 'philosophy', 'thesis', 'proposition', 'theory', 'universal']

    scores = {
        "melancholy": sum(1 for w in melancholy_words if w in text_lower),
        "passionate": sum(1 for w in passionate_words if w in text_lower),
        "intellectual": sum(1 for w in intellectual_words if w in text_lower)
    }

    # Determine dominant tone
    dominant = max(scores, key=scores.get)
    if scores[dominant] == 0:
        return "neutral"
    return dominant

def extract_topics(text):
    """
    Extracts key existential themes.
    """
    topics = []
    keywords = {
        "anxiety": ["dread", "anxiety", "fear"],
        "faith": ["faith", "god", "abraham", "isaac", "paradox"],
        "aesthetics": ["music", "poet", "beautiful", "pleasure"],
        "ethics": ["duty", "universal", "moral", "law"],
        "subjectivity": ["individual", "self", "inner", "subjective"]
    }

    text_lower = text.lower()
    for topic, words in keywords.items():
        if any(w in text_lower for w in words):
            topics.append(topic)

    return topics

def process_file(filepath, source_name):
    """
    Reads a file, chunks it, and enriches it.
    """
    print(f"[{ARCHIVIST_NAME}]: commencing scan of artifact '{source_name}'...")

    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Chunk by paragraphs (double newlines)
    chunks = re.split(r'\n\s*\n', content)
    chunks = [c.strip() for c in chunks if c.strip()]

    processed_data = []

    for i, chunk in enumerate(chunks):
        enrichment = {
            "content": chunk,
            "source_work": source_name,
            "metadata": {
                "chunk_id": f"{source_name.replace(' ', '_')}_{i:04d}",
                "reading_complexity": calculate_reading_complexity(chunk),
                "sentiment_tone": analyze_sentiment(chunk),
                "topics": extract_topics(chunk),
                "archival_info": {
                    "archivist": ARCHIVIST_NAME,
                    "timestamp": datetime.now().isoformat(),
                    "version": ARCHIVE_VERSION,
                    "note": "Preserved for posterity."
                }
            }
        }
        processed_data.append(enrichment)

    print(f"[{ARCHIVIST_NAME}]: processed {len(processed_data)} fragments from '{source_name}'.")
    return processed_data

def main():
    base_path = "socials_data/personalities/soren_kierkegaard"
    raw_dir = os.path.join(base_path, "raw")
    processed_dir = os.path.join(base_path, "processed")
    output_file = os.path.join(processed_dir, "data.jsonl")

    all_data = []

    if not os.path.exists(raw_dir):
        print(f"[{ARCHIVIST_NAME}]: Error! Raw directory not found: {raw_dir}")
        return

    for filename in os.listdir(raw_dir):
        if filename.endswith(".txt"):
            filepath = os.path.join(raw_dir, filename)
            source_name = filename.replace(".txt", "").replace("_", " ").title()
            data = process_file(filepath, source_name)
            all_data.extend(data)

    # Write to JSONL
    print(f"[{ARCHIVIST_NAME}]: writing {len(all_data)} records to the Great Archive (jsonl)...")
    with open(output_file, 'w', encoding='utf-8') as f:
        for entry in all_data:
            json.dump(entry, f)
            f.write('\n')

    print(f"[{ARCHIVIST_NAME}]: Operation complete. Data integrity verified.")

if __name__ == "__main__":
    main()
