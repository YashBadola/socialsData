import sqlite3
import json
import sys
import re
from pathlib import Path
from collections import Counter

def get_sentiment_score(text):
    """
    A very heuristic sentiment analysis for Schopenhauer.
    Negative words decrease score, positive increase.
    Schopenhauer should be mostly negative.
    """
    text = text.lower()
    negative_words = ["suffering", "pain", "tragedy", "loss", "absurd", "evil", "misfortune", "death", "boredom", "wretched", "worst"]
    positive_words = ["happiness", "pleasure", "joy", "good", "satisfied", "freedom", "morality", "compassion"]

    score = 0
    words = re.findall(r'\w+', text)
    if not words:
        return 0.0

    for word in words:
        if word in negative_words:
            score -= 1
        elif word in positive_words:
            score += 1

    # Normalize by length? Or just raw score. Let's do raw score normalized by length * 100 for readability
    return (score / len(words)) * 100

def extract_keywords(text):
    """
    Extracts top 5 keywords (excluding common stop words).
    """
    text = text.lower()
    stop_words = {"the", "and", "of", "to", "a", "in", "is", "that", "it", "as", "for", "with", "on", "be", "not", "this", "or", "but", "by", "are", "at", "from", "an", "so", "if", "we", "he", "his", "which", "will", "has", "have", "us", "no", "one", "him"}
    words = re.findall(r'\w+', text)
    filtered_words = [w for w in words if w not in stop_words and len(w) > 2]

    counts = Counter(filtered_words)
    return json.dumps([w for w, c in counts.most_common(5)])

def build_database(personality_id, base_dir=None):
    if base_dir is None:
        base_dir = Path("socials_data/personalities")
    else:
        base_dir = Path(base_dir)

    personality_dir = base_dir / personality_id

    if not personality_dir.exists():
        raise FileNotFoundError(f"Directory {personality_dir} does not exist.")

    data_file = personality_dir / "processed" / "data.jsonl"
    if not data_file.exists():
        raise FileNotFoundError(f"File {data_file} does not exist.")

    db_file = personality_dir / "database.db"

    # Initialize DB
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()

    # Create table
    cursor.execute("DROP TABLE IF EXISTS entries")
    cursor.execute("""
        CREATE TABLE entries (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            content TEXT,
            source TEXT,
            length INTEGER,
            sentiment_score REAL,
            keywords TEXT
        )
    """)

    print(f"Building database for {personality_id}...")

    count = 0
    with open(data_file, "r", encoding="utf-8") as f:
        for line in f:
            try:
                record = json.loads(line)
                text = record.get("text", "")
                source = record.get("source", "unknown")

                if not text:
                    continue

                length = len(text)
                sentiment = get_sentiment_score(text)
                keywords = extract_keywords(text)

                cursor.execute("""
                    INSERT INTO entries (content, source, length, sentiment_score, keywords)
                    VALUES (?, ?, ?, ?, ?)
                """, (text, source, length, sentiment, keywords))

                count += 1
            except json.JSONDecodeError:
                continue

    conn.commit()
    conn.close()

    print(f"Successfully inserted {count} entries into {db_file}")
    return db_file

def main():
    if len(sys.argv) < 2:
        print("Usage: python build_sqlite_db.py <personality_id>")
        sys.exit(1)

    personality_id = sys.argv[1]
    try:
        build_database(personality_id)
    except FileNotFoundError as e:
        print(f"Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
