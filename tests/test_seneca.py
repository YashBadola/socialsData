import pytest
import os
import json
from socials_data.core.manager import PersonalityManager
from socials_data import load_dataset

def test_seneca_exists():
    manager = PersonalityManager()
    personalities = manager.list_personalities()
    assert "seneca_the_younger" in personalities

def test_seneca_metadata():
    manager = PersonalityManager()
    metadata = manager.get_metadata("seneca_the_younger")
    assert metadata["name"] == "Seneca the Younger"
    assert metadata["id"] == "seneca_the_younger"
    assert "Epistulae Morales ad Lucilium" in [s["title"] for s in metadata["sources"]]

def test_seneca_data_loaded():
    dataset = load_dataset("seneca_the_younger")
    assert len(dataset) > 0

    # Check sample structure
    # load_dataset returns a Hugging Face Dataset, which supports indexing
    sample = dataset[0]
    assert "text" in sample
    assert "source" in sample

    # Check content
    all_text = " ".join([item["text"] for item in dataset])
    assert "short time to live" in all_text
    assert "bathing establishment" in all_text

def test_processed_file_integrity():
    processed_path = os.path.join("socials_data", "personalities", "seneca_the_younger", "processed", "data.jsonl")
    assert os.path.exists(processed_path)

    with open(processed_path, 'r') as f:
        lines = f.readlines()
        assert len(lines) == 2 # We added 2 files

        for line in lines:
            entry = json.loads(line)
            assert "text" in entry
            assert "source" in entry
            assert entry["source"] in ["on_shortness_of_life.txt", "letter_on_noise.txt"]
