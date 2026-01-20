import pytest
from socials_data.core.manager import PersonalityManager
import os
import json
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
    assert "The World as Will and Representation" in [s["title"] for s in metadata["sources"]]

def test_schopenhauer_data_loaded():
    dataset = load_dataset("arthur_schopenhauer")
    assert len(dataset) > 0

    # Check sample structure
    sample = dataset[0]
    assert "text" in sample
    assert "source" in sample
    assert sample["source"] == "world_as_will_excerpt.txt"
    assert "suffering" in sample["text"]

def test_schopenhauer_qa_exists():
    processed_path = os.path.join("socials_data", "personalities", "arthur_schopenhauer", "processed", "qa.jsonl")
    assert os.path.exists(processed_path)

    with open(processed_path, 'r') as f:
        lines = f.readlines()
        assert len(lines) > 0
        first_entry = json.loads(lines[0])
        assert "instruction" in first_entry
        assert "response" in first_entry
