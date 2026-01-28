import sqlite3
import re
from pathlib import Path
from collections import Counter

def build_db():
    base_dir = Path("socials_data/personalities/arthur_schopenhauer")
    raw_file = base_dir / "raw" / "on_the_sufferings_of_the_world.txt"
    processed_dir = base_dir / "processed"
    processed_dir.mkdir(parents=True, exist_ok=True)
    db_path = processed_dir / "knowledge.db"

    if db_path.exists():
        db_path.unlink()

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Define Schema
    cursor.execute("""
    CREATE TABLE sections (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT,
        content TEXT
    )
    """)

    cursor.execute("""
    CREATE TABLE paragraphs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        section_id INTEGER,
        content TEXT,
        sequence INTEGER,
        FOREIGN KEY(section_id) REFERENCES sections(id)
    )
    """)

    cursor.execute("""
    CREATE TABLE concepts (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        term TEXT UNIQUE,
        frequency INTEGER
    )
    """)

    cursor.execute("""
    CREATE TABLE concept_occurrences (
        concept_id INTEGER,
        paragraph_id INTEGER,
        FOREIGN KEY(concept_id) REFERENCES concepts(id),
        FOREIGN KEY(paragraph_id) REFERENCES paragraphs(id)
    )
    """)

    # Read and Process Text
    with open(raw_file, "r", encoding="utf-8") as f:
        text = f.read()

    # For this text, we don't have clear section headers, so we'll treat the whole text as one section
    # titled "On the Sufferings of the World"
    section_title = "On the Sufferings of the World"
    cursor.execute("INSERT INTO sections (title, content) VALUES (?, ?)", (section_title, text))
    section_id = cursor.lastrowid

    paragraphs = [p.strip() for p in text.split("\n\n") if p.strip()]

    # Concepts extraction: Find capitalized words that appear in the middle of sentences
    # This is a heuristic.
    concept_counter = Counter()

    # We will first populate paragraphs
    for idx, para_text in enumerate(paragraphs):
        cursor.execute("INSERT INTO paragraphs (section_id, content, sequence) VALUES (?, ?, ?)",
                       (section_id, para_text, idx))
        para_id = cursor.lastrowid

        # Extract potential concepts
        # Regex: words starting with uppercase, not at start of sentence (after . ? !), length > 3
        # Simplification: split by space, check if Capitalized.
        # To avoid sentence starters, we can check if the preceding token ends with punctuation.

        words = para_text.split()
        for i, word in enumerate(words):
            clean_word = word.strip('.,;:"\'()')
            if not clean_word:
                continue

            is_capitalized = clean_word[0].isupper()
            is_start_of_sentence = (i == 0) or (words[i-1].endswith(('.', '?', '!')))

            # Schopenhauer specific concepts often capitalized in translations: Will, Time, Fate, Nature, Evil, Good.
            # Also catch things that are capitalized even if at start, if they appear capitalized elsewhere in middle.
            # For simplicity in this heuristic: Capitalized AND (NOT start OR known_concepts)

            if is_capitalized and len(clean_word) > 3:
                # Store candidate
                if not is_start_of_sentence:
                    concept_counter[clean_word] += 1

                    # Store occurrence immediately? No, we need concept ID first.
                    # We'll do a second pass or handle it dynamically.
                    # Let's just collect occurrences in a list and insert later.

    # Filter concepts: appear at least once (as non-sentence starter)
    final_concepts = [term for term, count in concept_counter.items()]

    # Insert concepts
    term_to_id = {}
    for term in final_concepts:
        cursor.execute("INSERT INTO concepts (term, frequency) VALUES (?, ?)", (term, concept_counter[term]))
        term_to_id[term] = cursor.lastrowid

    # Second pass for occurrences (to catch them even at start of sentences if we wanted to be thorough,
    # but for now let's just map the ones we found to the paragraphs they are in)

    for idx, para_text in enumerate(paragraphs):
        # We need the para_id. We know sequence is idx.
        cursor.execute("SELECT id FROM paragraphs WHERE sequence = ? AND section_id = ?", (idx, section_id))
        para_id = cursor.fetchone()[0]

        for term, term_id in term_to_id.items():
            if term in para_text:
                cursor.execute("INSERT INTO concept_occurrences (concept_id, paragraph_id) VALUES (?, ?)",
                               (term_id, para_id))

    conn.commit()
    conn.close()
    print(f"Database built at {db_path}")
    print(f"Stats: {len(paragraphs)} paragraphs, {len(final_concepts)} concepts.")

if __name__ == "__main__":
    build_db()
