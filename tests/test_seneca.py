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
    assert "Moral Letters to Lucilius" in [s["title"] for s in metadata["sources"]]

def test_seneca_data_loaded():
    from socials_data import load_dataset
    dataset = load_dataset("seneca")
    assert len(dataset) > 0

    # Check sample structure
    # Since dataset is loaded via Hugging Face, it might be shuffled or not.
    # But we can iterate to find a specific source.
    found_letter = False
    for sample in dataset:
        if sample["source"] == "letter_1.txt":
            assert "ON SAVING TIME" in sample["text"]
            found_letter = True
            break

    assert found_letter

def test_processed_file_exists():
    processed_path = os.path.join("socials_data", "personalities", "seneca", "processed", "data.jsonl")
    assert os.path.exists(processed_path)

    with open(processed_path, 'r') as f:
        lines = f.readlines()
        assert len(lines) == 3
        first_entry = json.loads(lines[0])
        assert "text" in first_entry
        assert "source" in first_entry
