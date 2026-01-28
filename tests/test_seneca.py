import pytest
from socials_data.core.manager import PersonalityManager
import os
import json

def test_seneca_exists():
    manager = PersonalityManager()
    personalities = manager.list_personalities()
    assert "seneca" in personalities

def test_seneca_metadata():
    manager = PersonalityManager()
    metadata = manager.get_metadata("seneca")
    assert metadata["name"] == "Seneca"
    assert metadata["id"] == "seneca"
    source_titles = [s["title"] for s in metadata["sources"]]
    assert "On the Shortness of Life (De Brevitate Vitae)" in source_titles
    assert "On Anger (De Ira)" in source_titles

def test_seneca_data_loaded():
    from socials_data import load_dataset
    dataset = load_dataset("seneca")
    assert len(dataset) > 0

    # There should be 3 entries corresponding to our 3 files
    assert len(dataset) >= 3

    # Check for specific content
    texts = [d['text'] for d in dataset]
    combined_text = " ".join(texts)

    assert "Lucilius" in combined_text
    assert "Anger is a temporary madness" in combined_text
    assert "Life is long enough" in combined_text

def test_processed_file_exists():
    processed_path = os.path.join("socials_data", "personalities", "seneca", "processed", "data.jsonl")
    assert os.path.exists(processed_path)

    with open(processed_path, 'r') as f:
        lines = f.readlines()
        assert len(lines) >= 3
        first_entry = json.loads(lines[0])
        assert "text" in first_entry
        assert "source" in first_entry
