import sqlite3
import re
from pathlib import Path
import sys

def build_db():
    base_dir = Path(__file__).parent
    raw_dir = base_dir / "raw"
    processed_dir = base_dir / "processed"
    processed_dir.mkdir(parents=True, exist_ok=True)

    db_path = processed_dir / "aristotle.db"

    conn = sqlite3.connect(str(db_path))
    cursor = conn.cursor()

    # Create tables
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS works (
        id INTEGER PRIMARY KEY,
        title TEXT NOT NULL,
        description TEXT
    )
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS quotes (
        id INTEGER PRIMARY KEY,
        work_id INTEGER,
        text TEXT NOT NULL,
        topic TEXT,
        FOREIGN KEY(work_id) REFERENCES works(id)
    )
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS concepts (
        id INTEGER PRIMARY KEY,
        term TEXT NOT NULL,
        definition TEXT,
        source_work_id INTEGER,
        FOREIGN KEY(source_work_id) REFERENCES works(id)
    )
    ''')

    # Clear existing data to be safe
    cursor.execute('DELETE FROM concepts')
    cursor.execute('DELETE FROM quotes')
    cursor.execute('DELETE FROM works')

    # Seed data
    # 1. Nicomachean Ethics
    cursor.execute('INSERT INTO works (title, description) VALUES (?, ?)',
                   ("Nicomachean Ethics", "Aristotle's best-known work on ethics: the science of the good for human life."))
    ethics_id = cursor.lastrowid

    # Read raw file to find quotes
    ethics_file = raw_dir / "nicomachean_ethics_excerpt.txt"
    if ethics_file.exists():
        with open(ethics_file, 'r', encoding='utf-8') as f:
            content = f.read()

        # Naive extraction of "Golden Mean" quote
        mean_quote_match = re.search(r"(Virtue, then, is a state of character concerned with choice.*?an extreme\.)", content, re.DOTALL)
        if mean_quote_match:
            quote_text = mean_quote_match.group(1).replace('\n', ' ')
            cursor.execute('INSERT INTO quotes (work_id, text, topic) VALUES (?, ?, ?)',
                           (ethics_id, quote_text, "Virtue"))

        # Extract "Happiness/Good" quote
        good_quote_match = re.search(r"(If, then, there is some end of the things we do.*?chief good\.)", content, re.DOTALL)
        if good_quote_match:
            quote_text = good_quote_match.group(1).replace('\n', ' ')
            cursor.execute('INSERT INTO quotes (work_id, text, topic) VALUES (?, ?, ?)',
                           (ethics_id, quote_text, "The Good"))

    # Seed Concepts (Manual for this elaborate setup)
    concepts = [
        ("Eudaimonia", "Often translated as 'happiness' or 'flourishing'; the highest human good."),
        ("Phronesis", "Practical wisdom; the ability to deliberate well about what is good and expedient."),
        ("Golden Mean", "The desirable middle between two extremes, one of excess and the other of deficiency."),
        ("Telos", "The end, purpose, or goal of an action or object.")
    ]

    for term, definition in concepts:
        cursor.execute('INSERT INTO concepts (term, definition, source_work_id) VALUES (?, ?, ?)',
                       (term, definition, ethics_id))

    conn.commit()
    conn.close()
    print(f"Database built successfully at {db_path}")

if __name__ == "__main__":
    build_db()
