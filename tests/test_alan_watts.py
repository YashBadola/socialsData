import pytest
from socials_data.core.manager import PersonalityManager
import os
import json

def test_alan_watts_exists():
    manager = PersonalityManager()
    personalities = manager.list_personalities()
    assert "alan_watts" in personalities

def test_alan_watts_metadata():
    manager = PersonalityManager()
    metadata = manager.get_metadata("alan_watts")
    assert metadata["name"] == "Alan Watts"
    assert metadata["id"] == "alan_watts"
    assert "The Wisdom of Insecurity" in [s["title"] for s in metadata["sources"]]

def test_alan_watts_data_loaded():
    from socials_data import load_dataset
    dataset = load_dataset("alan_watts")
    assert len(dataset) > 0

    # Check sample structure
    sample = dataset[0]
    assert "text" in sample
    assert "source" in sample
    assert sample["source"] == "quotes.txt"

    assert isinstance(sample["text"], str)
    # The text we added is definitely longer than 100 chars
    assert len(sample["text"]) > 100

def test_processed_file_exists():
    processed_path = os.path.join("socials_data", "personalities", "alan_watts", "processed", "data.jsonl")
    assert os.path.exists(processed_path)

    with open(processed_path, 'r') as f:
        lines = f.readlines()
        assert len(lines) > 0
        first_entry = json.loads(lines[0])
        assert "text" in first_entry
        assert "source" in first_entry
