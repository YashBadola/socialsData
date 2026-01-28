import pytest
import sqlite3
import os
from pathlib import Path
from socials_data.core.manager import PersonalityManager
from socials_data import load_dataset

def test_schopenhauer_exists():
    manager = PersonalityManager()
    personalities = manager.list_personalities()
    assert "arthur_schopenhauer" in personalities

def test_schopenhauer_metadata():
    manager = PersonalityManager()
    metadata = manager.get_metadata("arthur_schopenhauer")
    assert metadata["name"] == "Arthur Schopenhauer"
    assert metadata["id"] == "arthur_schopenhauer"

def test_schopenhauer_dataset_load():
    dataset = load_dataset("arthur_schopenhauer")
    assert len(dataset) > 0
    sample = dataset[0]
    assert "text" in sample
    assert "source" in sample
    # The source name comes from the file name
    assert sample["source"] == "on_the_sufferings_of_the_world.txt"

def test_schopenhauer_elaborate_db():
    """Verify the elaborate SQLite database exists and is populated."""
    db_path = Path("socials_data/personalities/arthur_schopenhauer/processed/knowledge.db")
    assert db_path.exists(), "knowledge.db does not exist. Did you run build_schopenhauer_db.py?"

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Check sections
    cursor.execute("SELECT count(*) FROM sections")
    section_count = cursor.fetchone()[0]
    assert section_count >= 1

    # Check paragraphs
    cursor.execute("SELECT count(*) FROM paragraphs")
    para_count = cursor.fetchone()[0]
    assert para_count > 0

    # Check concepts
    cursor.execute("SELECT count(*) FROM concepts")
    concept_count = cursor.fetchone()[0]
    assert concept_count > 0

    conn.close()
