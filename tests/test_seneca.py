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
    assert metadata["name"] == "Seneca"
    assert metadata["id"] == "seneca"
    assert "Moral Letters to Lucilius" in [s["title"] for s in metadata["sources"]]

def test_seneca_data_loaded():
    from socials_data import load_dataset
    dataset = load_dataset("seneca")
    assert len(dataset) > 0

    # Check sample structure
    # Note: Dataset order is not guaranteed, so we check general properties
    sample = dataset[0]
    assert "text" in sample
    assert "source" in sample

    # We expect sources to be one of our created files
    expected_sources = [
        "on_saving_time.txt",
        "on_discursiveness_in_reading.txt",
        "on_true_and_false_friendship.txt",
        "on_the_shortness_of_life.txt"
    ]
    assert sample["source"] in expected_sources

    # Check for keywords from Seneca's style
    assert isinstance(sample["text"], str)
    assert len(sample["text"]) > 100

    # Iterate and find specific content to be sure
    all_text = " ".join([d["text"] for d in dataset])
    assert "Lucilius" in all_text
    assert "Nature" in all_text or "time" in all_text

def test_seneca_processed_file_exists():
    processed_path = os.path.join("socials_data", "personalities", "seneca", "processed", "data.jsonl")
    assert os.path.exists(processed_path)

    with open(processed_path, 'r') as f:
        lines = f.readlines()
        assert len(lines) == 4 # We created 4 files
        first_entry = json.loads(lines[0])
        assert "text" in first_entry
        assert "source" in first_entry
