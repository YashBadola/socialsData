import sqlite3
import json
import os
from pathlib import Path
import re

# Configuration
PERSONALITY_ID = "simone_de_beauvoir"
BASE_DIR = Path("socials_data/personalities") / PERSONALITY_ID
RAW_DIR = BASE_DIR / "raw"
PROCESSED_DIR = BASE_DIR / "processed"
DB_PATH = PROCESSED_DIR / "philosophy.db"
JSONL_PATH = PROCESSED_DIR / "data.jsonl"

def setup_database():
    """Creates the SQLite database and tables."""
    if DB_PATH.exists():
        os.remove(DB_PATH)

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Enable foreign keys
    cursor.execute("PRAGMA foreign_keys = ON;")

    # Create Tables
    cursor.execute("""
        CREATE TABLE excerpts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            content TEXT NOT NULL,
            source TEXT NOT NULL,
            sentiment TEXT
        );
    """)

    cursor.execute("""
        CREATE TABLE keywords (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            keyword TEXT UNIQUE NOT NULL
        );
    """)

    cursor.execute("""
        CREATE TABLE excerpt_keywords (
            excerpt_id INTEGER,
            keyword_id INTEGER,
            FOREIGN KEY(excerpt_id) REFERENCES excerpts(id),
            FOREIGN KEY(keyword_id) REFERENCES keywords(id),
            PRIMARY KEY (excerpt_id, keyword_id)
        );
    """)

    conn.commit()
    return conn

def extract_keywords(text):
    """Simulated keyword extraction."""
    potential_keywords = ["woman", "freedom", "ambiguity", "other", "existence", "essence", "civilization", "fate", "sub-man"]
    found_keywords = [k for k in potential_keywords if k.lower() in text.lower()]
    return found_keywords

def analyze_sentiment(text):
    """Simulated sentiment analysis."""
    if "freedom" in text.lower() or "future" in text.lower():
        return "inspiring"
    elif "tragic" in text.lower() or "afraid" in text.lower():
        return "somber"
    else:
        return "neutral"

def process_files(conn):
    """Reads raw files, chunks them, and inserts into DB."""
    cursor = conn.cursor()

    raw_files = list(RAW_DIR.glob("*.txt"))
    if not raw_files:
        print(f"No raw files found in {RAW_DIR}")
        return

    jsonl_data = []

    for file_path in raw_files:
        print(f"Processing {file_path.name}...")
        with open(file_path, "r", encoding="utf-8") as f:
            text = f.read()

        # Split by double newlines to simulate paragraph chunks
        chunks = [c.strip() for c in text.split("\n\n") if c.strip()]

        for chunk in chunks:
            if len(chunk) < 20: continue # Skip titles or garbage

            sentiment = analyze_sentiment(chunk)
            keywords = extract_keywords(chunk)

            # Insert into Excerpts
            cursor.execute("INSERT INTO excerpts (content, source, sentiment) VALUES (?, ?, ?)",
                           (chunk, file_path.name, sentiment))
            excerpt_id = cursor.lastrowid

            # Insert Keywords
            for kw in keywords:
                cursor.execute("INSERT OR IGNORE INTO keywords (keyword) VALUES (?)", (kw,))
                cursor.execute("SELECT id FROM keywords WHERE keyword = ?", (kw,))
                keyword_id = cursor.fetchone()[0]

                cursor.execute("INSERT OR IGNORE INTO excerpt_keywords (excerpt_id, keyword_id) VALUES (?, ?)",
                               (excerpt_id, keyword_id))

            # Prepare data for JSONL (backward compatibility)
            jsonl_data.append({
                "text": chunk,
                "source": file_path.name,
                "metadata": {
                    "sentiment": sentiment,
                    "keywords": keywords
                }
            })

    conn.commit()
    return jsonl_data

def save_jsonl(data):
    """Saves the processed data to a JSONL file."""
    with open(JSONL_PATH, "w", encoding="utf-8") as f:
        for entry in data:
            f.write(json.dumps(entry) + "\n")
    print(f"Saved {len(data)} records to {JSONL_PATH}")

def main():
    print(f"Starting processing for {PERSONALITY_ID}...")

    if not PROCESSED_DIR.exists():
        PROCESSED_DIR.mkdir(parents=True)

    conn = setup_database()
    try:
        data = process_files(conn)
        save_jsonl(data)
    finally:
        conn.close()

    print("Processing complete.")

if __name__ == "__main__":
    main()
