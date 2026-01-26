import pytest
from socials_data.core.manager import PersonalityManager
import os
import json

def test_soren_kierkegaard_exists():
    manager = PersonalityManager()
    personalities = manager.list_personalities()
    assert "soren_kierkegaard" in personalities

def test_soren_kierkegaard_metadata():
    manager = PersonalityManager()
    metadata = manager.get_metadata("soren_kierkegaard")
    assert metadata["name"] == "Søren Kierkegaard"
    assert metadata["id"] == "soren_kierkegaard"
    titles = [s["title"] for s in metadata["sources"]]
    assert "Fear and Trembling" in titles
    assert "The Sickness Unto Death" in titles

def test_soren_kierkegaard_data_loaded():
    from socials_data import load_dataset
    dataset = load_dataset("soren_kierkegaard")
    assert len(dataset) > 0

    # Check sample structure
    sample = dataset[0]
    assert "text" in sample
    assert "source" in sample
    # Check that source is one of the files we added
    assert sample["source"] in ["fear_and_trembling.txt", "sickness_unto_death.txt"]

def test_processed_file_exists():
    processed_path = os.path.join("socials_data", "personalities", "soren_kierkegaard", "processed", "data.jsonl")
    assert os.path.exists(processed_path)

    with open(processed_path, 'r') as f:
        lines = f.readlines()
        assert len(lines) > 0
        first_entry = json.loads(lines[0])
        assert "text" in first_entry
        assert "source" in first_entry
