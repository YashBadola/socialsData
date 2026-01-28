import pytest
from socials_data.core.manager import PersonalityManager
import os
import json
from socials_data import load_dataset

def test_seneca_exists():
    manager = PersonalityManager()
    personalities = manager.list_personalities()
    assert "seneca" in personalities

def test_seneca_metadata():
    manager = PersonalityManager()
    metadata = manager.get_metadata("seneca")
    assert metadata["name"] == "Seneca"
    assert metadata["id"] == "seneca"
    titles = [s["title"] for s in metadata["sources"]]
    assert "On the Shortness of Life (De Brevitate Vitae)" in titles
    assert "Moral Letters to Lucilius (Epistulae Morales ad Lucilium)" in titles

def test_seneca_data_loaded():
    dataset = load_dataset("seneca")
    assert len(dataset) > 0

    # Check sample structure
    sample = dataset[0]
    assert "text" in sample
    assert "source" in sample
    # Check that sources are from the ones we added
    assert sample["source"] in [
        "on_shortness_of_life.txt",
        "letter_13_on_groundless_fears.txt",
        "letter_101_on_futility_of_planning_ahead.txt"
    ]

    assert isinstance(sample["text"], str)
    assert len(sample["text"]) > 100

def test_seneca_processed_file_content():
    processed_path = os.path.join("socials_data", "personalities", "seneca", "processed", "data.jsonl")
    assert os.path.exists(processed_path)

    with open(processed_path, 'r') as f:
        lines = f.readlines()
        assert len(lines) == 3 # We created 3 files, processed into 3 records

        sources = set()
        for line in lines:
            entry = json.loads(line)
            sources.add(entry["source"])

        assert "on_shortness_of_life.txt" in sources
        assert "letter_13_on_groundless_fears.txt" in sources
        assert "letter_101_on_futility_of_planning_ahead.txt" in sources
