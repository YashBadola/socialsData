import pytest
from socials_data.core.manager import PersonalityManager
import os
import json
from socials_data import load_dataset

def test_seneca_exists():
    manager = PersonalityManager()
    personalities = manager.list_personalities()
    assert "lucius_annaeus_seneca" in personalities

def test_seneca_metadata():
    manager = PersonalityManager()
    metadata = manager.get_metadata("lucius_annaeus_seneca")
    assert metadata["name"] == "Lucius Annaeus Seneca"
    assert metadata["id"] == "lucius_annaeus_seneca"
    assert "Moral Letters to Lucilius" in [s["title"] for s in metadata["sources"]]

def test_seneca_data_loaded():
    dataset = load_dataset("lucius_annaeus_seneca")
    assert len(dataset) > 0

    # Check sample structure
    sample = dataset[0]
    assert "text" in sample
    assert "source" in sample
    # The source name will be one of the letter files
    assert sample["source"].startswith("letter_")

    assert isinstance(sample["text"], str)
    assert len(sample["text"]) > 100

def test_processed_file_exists():
    processed_path = os.path.join("socials_data", "personalities", "lucius_annaeus_seneca", "processed", "data.jsonl")
    assert os.path.exists(processed_path)

    with open(processed_path, 'r') as f:
        lines = f.readlines()
        assert len(lines) > 0
        first_entry = json.loads(lines[0])
        assert "text" in first_entry
        assert "source" in first_entry
