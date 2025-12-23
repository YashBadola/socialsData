import pytest
from socials_data.core.manager import PersonalityManager
import os
import json

def test_john_stuart_mill_exists():
    manager = PersonalityManager()
    personalities = manager.list_personalities()
    assert "john_stuart_mill" in personalities

def test_john_stuart_mill_metadata():
    manager = PersonalityManager()
    metadata = manager.get_metadata("john_stuart_mill")
    assert metadata["name"] == "John Stuart Mill"
    assert metadata["id"] == "john_stuart_mill"
    assert "On Liberty" in [s["title"] for s in metadata["sources"]]

def test_john_stuart_mill_data_loaded():
    from socials_data import load_dataset
    dataset = load_dataset("john_stuart_mill")
    assert len(dataset) > 0

    # Check sample structure
    sample = dataset[0]
    assert "text" in sample
    assert "source" in sample
    assert sample["source"] == "on_liberty.txt"

    # Check for keywords from "On Liberty"
    # Note: Text chunking might split the text, but "liberty" or "individual" should appear frequently.
    # We will just check if text is a string and has reasonable length.
    assert isinstance(sample["text"], str)
    assert len(sample["text"]) > 100

def test_processed_file_exists():
    processed_path = os.path.join("socials_data", "personalities", "john_stuart_mill", "processed", "data.jsonl")
    assert os.path.exists(processed_path)

    with open(processed_path, 'r') as f:
        lines = f.readlines()
        assert len(lines) > 0
        first_entry = json.loads(lines[0])
        assert "text" in first_entry
        assert "source" in first_entry
