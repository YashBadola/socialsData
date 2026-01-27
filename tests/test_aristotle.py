import pytest
from socials_data.core.manager import PersonalityManager
import os
import json

def test_aristotle_exists():
    manager = PersonalityManager()
    personalities = manager.list_personalities()
    assert "aristotle" in personalities

def test_aristotle_metadata():
    manager = PersonalityManager()
    metadata = manager.get_metadata("aristotle")
    assert metadata["name"] == "Aristotle"
    assert metadata["id"] == "aristotle"
    titles = [s["title"] for s in metadata["sources"]]
    assert "Nicomachean Ethics" in titles
    assert "Politics" in titles

def test_aristotle_data_loaded():
    from socials_data import load_dataset
    dataset = load_dataset("aristotle")
    assert len(dataset) > 0

    # Check sample structure
    # Since the order isn't guaranteed, we iterate to check.
    sources = set()
    for item in dataset:
        assert "text" in item
        assert "source" in item
        sources.add(item["source"])

    assert "nicomachean_ethics.txt" in sources
    assert "politics.txt" in sources

def test_processed_file_exists():
    processed_path = os.path.join("socials_data", "personalities", "aristotle", "processed", "data.jsonl")
    assert os.path.exists(processed_path)

    with open(processed_path, 'r') as f:
        lines = f.readlines()
        assert len(lines) >= 2
        for line in lines:
            entry = json.loads(line)
            assert "text" in entry
            assert "source" in entry
