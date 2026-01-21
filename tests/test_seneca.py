import pytest
from socials_data.core.manager import PersonalityManager
import os
import json

def test_seneca_exists():
    manager = PersonalityManager()
    personalities = manager.list_personalities()
    assert "seneca" in personalities

def test_seneca_metadata():
    manager = PersonalityManager()
    metadata = manager.get_metadata("seneca")
    assert metadata["name"] == "Seneca the Younger"
    assert metadata["id"] == "seneca"
    assert "Letters from a Stoic (Epistulae Morales ad Lucilium)" in [s["title"] for s in metadata["sources"]]

def test_seneca_data_loaded():
    from socials_data import load_dataset
    dataset = load_dataset("seneca")
    assert len(dataset) > 0

    # Check sample structure
    sample = dataset[0]
    assert "text" in sample
    assert "source" in sample
    assert sample["source"] == "letters.txt"

    assert isinstance(sample["text"], str)
    assert len(sample["text"]) > 100

def test_processed_file_exists():
    processed_path = os.path.join("socials_data", "personalities", "seneca", "processed", "data.jsonl")
    assert os.path.exists(processed_path)

    with open(processed_path, 'r') as f:
        lines = f.readlines()
        assert len(lines) > 0
        first_entry = json.loads(lines[0])
        assert "text" in first_entry
        assert "source" in first_entry

def test_qa_file_exists_and_valid():
    qa_path = os.path.join("socials_data", "personalities", "seneca", "processed", "qa.jsonl")
    assert os.path.exists(qa_path)

    with open(qa_path, 'r') as f:
        lines = f.readlines()
        assert len(lines) > 0
        for line in lines:
            entry = json.loads(line)
            assert "instruction" in entry
            assert "response" in entry
            assert len(entry["instruction"]) > 0
            assert len(entry["response"]) > 0
