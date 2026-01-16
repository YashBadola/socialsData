import pytest
from socials_data.core.manager import PersonalityManager
import os
import json

def test_arthur_schopenhauer_exists():
    manager = PersonalityManager()
    personalities = manager.list_personalities()
    assert "arthur_schopenhauer" in personalities

def test_arthur_schopenhauer_metadata():
    manager = PersonalityManager()
    metadata = manager.get_metadata("arthur_schopenhauer")
    assert metadata["name"] == "Arthur Schopenhauer"
    assert metadata["id"] == "arthur_schopenhauer"
    assert "The World as Will and Representation" in [s["title"] for s in metadata["sources"]]

def test_arthur_schopenhauer_data_loaded():
    from socials_data import load_dataset
    dataset = load_dataset("arthur_schopenhauer")
    assert len(dataset) > 0

    # Check sample structure
    sample = dataset[0]
    assert "text" in sample
    assert "source" in sample
    assert sample["source"] == "world_as_will_excerpt.txt"

    assert isinstance(sample["text"], str)
    assert len(sample["text"]) > 100
    assert "representation" in sample["text"].lower()

def test_processed_file_exists():
    processed_path = os.path.join("socials_data", "personalities", "arthur_schopenhauer", "processed", "data.jsonl")
    assert os.path.exists(processed_path)

    with open(processed_path, 'r') as f:
        lines = f.readlines()
        assert len(lines) > 0
        first_entry = json.loads(lines[0])
        assert "text" in first_entry
        assert "source" in first_entry
