import pytest
from socials_data.core.manager import PersonalityManager
import os
import json

def test_diogenes_exists():
    manager = PersonalityManager()
    personalities = manager.list_personalities()
    assert "diogenes_of_sinope" in personalities

def test_diogenes_metadata():
    manager = PersonalityManager()
    metadata = manager.get_metadata("diogenes_of_sinope")
    assert metadata["name"] == "Diogenes of Sinope"
    assert metadata["id"] == "diogenes_of_sinope"
    assert "Lives and Opinions of Eminent Philosophers (Book VI)" in [s["title"] for s in metadata["sources"]]

def test_diogenes_data_loaded():
    from socials_data import load_dataset
    dataset = load_dataset("diogenes_of_sinope")
    assert len(dataset) > 0

    # Check sample structure
    sample = dataset[0]
    assert "text" in sample
    assert "source" in sample
    assert sample["source"] == "sayings_and_anecdotes.txt"

    # Check content
    assert isinstance(sample["text"], str)
    assert len(sample["text"]) > 100
    assert "Diogenes" in sample["text"]

def test_processed_file_exists():
    processed_path = os.path.join("socials_data", "personalities", "diogenes_of_sinope", "processed", "data.jsonl")
    assert os.path.exists(processed_path)

    with open(processed_path, 'r') as f:
        lines = f.readlines()
        assert len(lines) > 0
        first_entry = json.loads(lines[0])
        assert "text" in first_entry
        assert "source" in first_entry

def test_qa_file_exists():
    qa_path = os.path.join("socials_data", "personalities", "diogenes_of_sinope", "processed", "qa.jsonl")
    assert os.path.exists(qa_path)

    with open(qa_path, 'r') as f:
        lines = f.readlines()
        assert len(lines) > 0
        first_entry = json.loads(lines[0])
        assert "instruction" in first_entry
        assert "response" in first_entry
