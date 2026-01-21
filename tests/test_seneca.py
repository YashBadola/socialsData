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
    assert metadata["name"] == "Lucius Annaeus Seneca"
    assert metadata["id"] == "seneca"
    assert "Letters from a Stoic (Epistulae Morales ad Lucilium)" in [s["title"] for s in metadata["sources"]]

def test_seneca_data_loaded():
    from socials_data import load_dataset
    dataset = load_dataset("seneca")
    assert len(dataset) == 3

    # Check sample structure
    sample = dataset[0]
    assert "text" in sample
    assert "source" in sample
    # The order might depend on file system listing, so we just check it is one of the files
    assert sample["source"] in ["letter_1_on_saving_time.txt", "letter_7_on_crowds.txt", "on_anger_excerpt.txt"]

    assert isinstance(sample["text"], str)
    assert len(sample["text"]) > 100

def test_processed_file_exists():
    processed_path = os.path.join("socials_data", "personalities", "seneca", "processed", "data.jsonl")
    assert os.path.exists(processed_path)

    with open(processed_path, 'r') as f:
        lines = f.readlines()
        assert len(lines) == 3
        first_entry = json.loads(lines[0])
        assert "text" in first_entry
        assert "source" in first_entry
