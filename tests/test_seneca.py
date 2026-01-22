import pytest
from socials_data.core.manager import PersonalityManager
import os
import json

def test_seneca_exists():
    manager = PersonalityManager()
    personalities = manager.list_personalities()
    assert "seneca_the_younger" in personalities

def test_seneca_metadata():
    manager = PersonalityManager()
    metadata = manager.get_metadata("seneca_the_younger")
    assert metadata["name"] == "Seneca the Younger"
    assert metadata["id"] == "seneca_the_younger"
    assert "De Brevitate Vitae" in [s["title"] for s in metadata["sources"]]

def test_seneca_data_loaded():
    from socials_data import load_dataset
    dataset = load_dataset("seneca_the_younger")
    assert len(dataset) > 0

    # Check sample structure
    sample = dataset[0]
    assert "text" in sample
    assert "source" in sample
    # We can't guarantee order, so we check if source is one of the expected files
    assert sample["source"] in ["on_shortness_of_life.txt", "letter_on_noise.txt"]

    # Check for keywords
    text_blob = " ".join([d["text"] for d in dataset])
    assert "short time to live" in text_blob
    assert "bathing establishment" in text_blob

def test_processed_file_exists():
    processed_path = os.path.join("socials_data", "personalities", "seneca_the_younger", "processed", "data.jsonl")
    assert os.path.exists(processed_path)

    with open(processed_path, 'r') as f:
        lines = f.readlines()
        assert len(lines) >= 2 # We added 2 files
        first_entry = json.loads(lines[0])
        assert "text" in first_entry
        assert "source" in first_entry
