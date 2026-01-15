from socials_data import load_dataset
from socials_data.core.exporter import SQLiteExporter
from pathlib import Path
import sqlite3
import os

def test_wittgenstein_dataset():
    """Test that the Wittgenstein dataset loads correctly."""
    ds = load_dataset("ludwig_wittgenstein")
    assert len(ds) == 2
    all_text = " ".join([item["text"] for item in ds])
    assert "The world is everything that is the case" in all_text
    assert "meaning of a word is its use in the language" in all_text

def test_sqlite_export():
    """Test that the SQLite export works by running it."""
    personality_dir = Path("socials_data/personalities/ludwig_wittgenstein")
    exporter = SQLiteExporter(personality_dir)

    # Run the export
    db_path = exporter.export()

    assert db_path.exists()

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Check personality table
    cursor.execute("SELECT name, system_prompt FROM personality")
    row = cursor.fetchone()
    assert row[0] == "Ludwig Wittgenstein"
    assert "You are Ludwig Wittgenstein" in row[1]

    # Check writings table
    cursor.execute("SELECT count(*) FROM writings")
    count = cursor.fetchone()[0]
    assert count == 2

    conn.close()

    # Clean up
    os.remove(db_path)

if __name__ == "__main__":
    test_wittgenstein_dataset()
    test_sqlite_export()
    print("Wittgenstein and Export tests passed!")
