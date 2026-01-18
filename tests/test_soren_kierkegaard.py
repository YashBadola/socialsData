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
    assert metadata["name"] == "Soren Kierkegaard"
    assert metadata["id"] == "soren_kierkegaard"
    assert "Fear and Trembling" in [s["title"] for s in metadata["sources"]]

def test_soren_kierkegaard_data_loaded():
    from socials_data import load_dataset
    dataset = load_dataset("soren_kierkegaard")
    assert len(dataset) > 0

    # Check sample structure
    sample = dataset[0]
    assert "text" in sample
    assert "source" in sample
    assert sample["source"] == "fear_and_trembling_excerpt.txt"

    assert isinstance(sample["text"], str)
    assert len(sample["text"]) > 100
    assert "Knight of Faith" in sample["text"]

def test_processed_file_exists():
    processed_path = os.path.join("socials_data", "personalities", "soren_kierkegaard", "processed", "data.jsonl")
    assert os.path.exists(processed_path)

    with open(processed_path, 'r') as f:
        lines = f.readlines()
        assert len(lines) > 0
        first_entry = json.loads(lines[0])
        assert "text" in first_entry
        assert "source" in first_entry

def test_qa_file_exists_and_valid():
    qa_path = os.path.join("socials_data", "personalities", "soren_kierkegaard", "processed", "qa.jsonl")
    assert os.path.exists(qa_path)

    with open(qa_path, 'r') as f:
        lines = f.readlines()
        assert len(lines) >= 5 # We added 5
        first_entry = json.loads(lines[0])
        assert "instruction" in first_entry
        assert "response" in first_entry
