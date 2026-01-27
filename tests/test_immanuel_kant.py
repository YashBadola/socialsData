import pytest
from socials_data.core.manager import PersonalityManager
import os
import json

def test_immanuel_kant_exists():
    manager = PersonalityManager()
    personalities = manager.list_personalities()
    assert "immanuel_kant" in personalities

def test_immanuel_kant_metadata():
    manager = PersonalityManager()
    metadata = manager.get_metadata("immanuel_kant")
    assert metadata["name"] == "Immanuel Kant"
    assert metadata["id"] == "immanuel_kant"
    assert "Fundamental Principles of the Metaphysic of Morals" in [s["title"] for s in metadata["sources"]]

def test_immanuel_kant_data_loaded():
    from socials_data import load_dataset
    dataset = load_dataset("immanuel_kant")
    assert len(dataset) > 0

    # Check sample structure
    # Since we added two files, the order might vary depending on OS iteration order,
    # but we can check if the source is one of the expected ones.
    sample = dataset[0]
    assert "text" in sample
    assert "source" in sample
    assert sample["source"] in ["fundamental_principles.txt", "critique_pure_reason.txt"]

    # Check for keywords
    assert isinstance(sample["text"], str)
    assert len(sample["text"]) > 100

def test_processed_file_exists():
    processed_path = os.path.join("socials_data", "personalities", "immanuel_kant", "processed", "data.jsonl")
    assert os.path.exists(processed_path)

    with open(processed_path, 'r') as f:
        lines = f.readlines()
        assert len(lines) >= 2 # We have at least 2 entries (one from each file)
        first_entry = json.loads(lines[0])
        assert "text" in first_entry
        assert "source" in first_entry
