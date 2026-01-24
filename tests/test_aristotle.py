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
    assert "Nicomachean Ethics" in [s["title"] for s in metadata["sources"]]
    assert "Politics" in [s["title"] for s in metadata["sources"]]
    assert "Poetics" in [s["title"] for s in metadata["sources"]]

def test_aristotle_data_loaded():
    from socials_data import load_dataset
    dataset = load_dataset("aristotle")
    assert len(dataset) > 0

    # Check sample structure
    sample = dataset[0]
    assert "text" in sample
    assert "source" in sample
    # The source should be one of the files we created
    assert sample["source"] in ["nicomachean_ethics.txt", "politics.txt", "poetics.txt"]

    assert isinstance(sample["text"], str)
    assert len(sample["text"]) > 100

def test_processed_file_exists():
    processed_path = os.path.join("socials_data", "personalities", "aristotle", "processed", "data.jsonl")
    assert os.path.exists(processed_path)

    with open(processed_path, 'r') as f:
        lines = f.readlines()
        assert len(lines) > 0
        first_entry = json.loads(lines[0])
        assert "text" in first_entry
        assert "source" in first_entry

if __name__ == "__main__":
    test_aristotle_exists()
    test_aristotle_metadata()
    test_aristotle_data_loaded()
    test_processed_file_exists()
    print("All tests passed!")
