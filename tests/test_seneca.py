import pytest
from socials_data.core.manager import PersonalityManager
from socials_data import load_dataset
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
    assert "Letters from a Stoic" in [s["title"] for s in metadata["sources"]]

def test_seneca_data_loaded():
    dataset = load_dataset("seneca")
    assert len(dataset) >= 3  # We added 3 letters

    # Check that we have the specific letters
    sources = set(dataset["source"])
    assert "letter_1.txt" in sources
    assert "letter_7.txt" in sources
    assert "letter_13.txt" in sources

    # Check content of one letter
    letter_1 = [d for d in dataset if d["source"] == "letter_1.txt"][0]
    assert "Greetings from Seneca" in letter_1["text"]
    assert "Farewell" in letter_1["text"]

def test_processed_file_exists():
    processed_path = os.path.join("socials_data", "personalities", "seneca", "processed", "data.jsonl")
    assert os.path.exists(processed_path)

    with open(processed_path, 'r') as f:
        lines = f.readlines()
        assert len(lines) >= 3
