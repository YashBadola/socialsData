import pytest
from socials_data.core.manager import PersonalityManager
import os
import json
from socials_data import load_dataset

def test_soren_kierkegaard_exists():
    manager = PersonalityManager()
    personalities = manager.list_personalities()
    assert "soren_kierkegaard" in personalities

def test_soren_kierkegaard_metadata():
    manager = PersonalityManager()
    metadata = manager.get_metadata("soren_kierkegaard")
    assert metadata["name"] == "Søren Kierkegaard"
    assert metadata["id"] == "soren_kierkegaard"
    assert "Selections from the Writings of Kierkegaard" in [s["title"] for s in metadata["sources"]]

def test_soren_kierkegaard_data_loaded():
    dataset = load_dataset("soren_kierkegaard")
    assert len(dataset) > 0

    sample = dataset[0]
    assert "text" in sample
    assert "source" in sample
    assert sample["source"] == "selections.txt"

    assert isinstance(sample["text"], str)
    assert len(sample["text"]) > 100

def test_qa_file_exists_and_valid():
    qa_path = os.path.join("socials_data", "personalities", "soren_kierkegaard", "processed", "qa.jsonl")
    assert os.path.exists(qa_path)

    with open(qa_path, 'r') as f:
        lines = f.readlines()
        assert len(lines) > 0
        first_entry = json.loads(lines[0])
        assert "instruction" in first_entry
        assert "response" in first_entry
        assert "source" in first_entry
