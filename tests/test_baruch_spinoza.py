import pytest
from socials_data.core.manager import PersonalityManager
import os
import json

def test_baruch_spinoza_exists():
    manager = PersonalityManager()
    personalities = manager.list_personalities()
    assert "baruch_spinoza" in personalities

def test_baruch_spinoza_metadata():
    manager = PersonalityManager()
    metadata = manager.get_metadata("baruch_spinoza")
    assert metadata["name"] == "Baruch Spinoza"
    assert metadata["id"] == "baruch_spinoza"
    assert "Ethics" in [s["title"] for s in metadata["sources"]]

def test_baruch_spinoza_data_loaded():
    from socials_data import load_dataset
    dataset = load_dataset("baruch_spinoza")
    assert len(dataset) > 0

    # Check sample structure
    # We don't know the exact order, but we can check if we have entries from different files
    sources = set()
    for item in dataset:
        assert "text" in item
        assert "source" in item
        sources.add(item["source"])

    assert "ethics_part1_definitions.txt" in sources
    assert "ethics_part1_propositions.txt" in sources

    # Check for keywords from Ethics
    first_text = dataset[0]["text"]
    assert isinstance(first_text, str)
    assert len(first_text) > 20

def test_processed_file_exists():
    processed_path = os.path.join("socials_data", "personalities", "baruch_spinoza", "processed", "data.jsonl")
    assert os.path.exists(processed_path)

    with open(processed_path, 'r') as f:
        lines = f.readlines()
        assert len(lines) >= 4 # We created 4 files
        first_entry = json.loads(lines[0])
        assert "text" in first_entry
        assert "source" in first_entry
