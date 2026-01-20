import pytest
from socials_data.core.manager import PersonalityManager
import os
import json

def test_albert_camus_exists():
    manager = PersonalityManager()
    personalities = manager.list_personalities()
    assert "albert_camus" in personalities

def test_albert_camus_metadata():
    manager = PersonalityManager()
    metadata = manager.get_metadata("albert_camus")
    assert metadata["name"] == "Albert Camus"
    assert metadata["id"] == "albert_camus"
    assert "The Myth of Sisyphus" in [s["title"] for s in metadata["sources"]]

def test_albert_camus_data_loaded():
    from socials_data import load_dataset
    dataset = load_dataset("albert_camus")
    assert len(dataset) > 0

    # Check sample structure
    sample = dataset[0]
    assert "text" in sample
    assert "source" in sample
    # The first processed file might vary depending on order, but it should be one of them
    assert sample["source"] in ["myth_of_sisyphus.txt", "the_stranger.txt", "quotes.txt"]

    assert isinstance(sample["text"], str)
    assert len(sample["text"]) > 10

def test_processed_file_exists():
    processed_path = os.path.join("socials_data", "personalities", "albert_camus", "processed", "data.jsonl")
    assert os.path.exists(processed_path)

    with open(processed_path, 'r') as f:
        lines = f.readlines()
        assert len(lines) > 0
        first_entry = json.loads(lines[0])
        assert "text" in first_entry
        assert "source" in first_entry

def test_qa_file_exists_and_valid():
    qa_path = os.path.join("socials_data", "personalities", "albert_camus", "processed", "qa.jsonl")
    assert os.path.exists(qa_path)

    with open(qa_path, 'r') as f:
        lines = f.readlines()
        assert len(lines) > 0
        first_entry = json.loads(lines[0])
        assert "instruction" in first_entry
        assert "response" in first_entry
