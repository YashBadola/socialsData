import pytest
import sqlite3
import shutil
import json
from pathlib import Path
from scripts.build_sqlite_db import get_sentiment_score, extract_keywords, build_database

def test_sentiment_score():
    assert get_sentiment_score("suffering pain") < 0
    assert get_sentiment_score("happiness joy") > 0
    assert get_sentiment_score("table chair") == 0

def test_extract_keywords():
    text = "apple apple apple orange orange banana"
    keywords = json.loads(extract_keywords(text))
    assert "apple" in keywords
    assert "orange" in keywords
    assert "banana" in keywords

def test_integration(tmp_path):
    # Setup
    base_dir = tmp_path / "personalities"
    personality_dir = base_dir / "test_p"
    (personality_dir / "processed").mkdir(parents=True)

    data_file = personality_dir / "processed" / "data.jsonl"
    with open(data_file, "w") as f:
        f.write(json.dumps({"text": "suffering and pain", "source": "test"}) + "\n")

    # Execute
    db_file = build_database("test_p", base_dir=base_dir)

    # Verify
    assert db_file.exists()

    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()
    cursor.execute("SELECT content, sentiment_score FROM entries")
    row = cursor.fetchone()

    assert row is not None
    assert row[0] == "suffering and pain"
    assert row[1] < 0  # Should be negative due to "suffering", "pain"

    conn.close()
