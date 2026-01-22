import pytest
from socials_data.core.manager import PersonalityManager
import os
import json

def test_soren_kierkegaard_exists():
    manager = PersonalityManager()
    personalities = manager.list_personalities()
    assert "søren_kierkegaard" in personalities

def test_soren_kierkegaard_metadata():
    manager = PersonalityManager()
    metadata = manager.get_metadata("søren_kierkegaard")
    assert metadata["name"] == "Søren Kierkegaard"
    assert metadata["id"] == "søren_kierkegaard"
    assert "Fear and Trembling" in [s["title"] for s in metadata["sources"]]

def test_soren_kierkegaard_data_loaded():
    from socials_data import load_dataset
    dataset = load_dataset("søren_kierkegaard")
    assert len(dataset) > 0

    # Check sample structure
    sample = dataset[0]
    assert "text" in sample
    assert "source" in sample
    assert sample["source"] == "fear_and_trembling_excerpt.txt"

    # Check for keywords
    assert isinstance(sample["text"], str)
    assert len(sample["text"]) > 100
    assert "faith" in sample["text"] or "ethical" in sample["text"]

def test_processed_file_exists():
    processed_path = os.path.join("socials_data", "personalities", "søren_kierkegaard", "processed", "data.jsonl")
    assert os.path.exists(processed_path)

    with open(processed_path, 'r') as f:
        lines = f.readlines()
        assert len(lines) > 0
        first_entry = json.loads(lines[0])
        assert "text" in first_entry
        assert "source" in first_entry
