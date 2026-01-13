import pytest
from socials_data.core.manager import PersonalityManager
import os
import json

def test_vitruvius_exists():
    manager = PersonalityManager()
    personalities = manager.list_personalities()
    assert "vitruvius" in personalities

def test_vitruvius_metadata():
    manager = PersonalityManager()
    metadata = manager.get_metadata("vitruvius")
    assert metadata["name"] == "Marcus Vitruvius Pollio"
    assert metadata["id"] == "vitruvius"
    assert "De Architectura (The Ten Books on Architecture)" in [s["title"] for s in metadata["sources"]]

def test_vitruvius_data_loaded():
    from socials_data import load_dataset
    dataset = load_dataset("vitruvius")
    assert len(dataset) > 0

    # Check sample structure
    sample = dataset[0]
    assert "text" in sample
    assert "source" in sample
    assert sample["source"] == "de_architectura_excerpts.txt"

    # Check for keywords
    assert isinstance(sample["text"], str)
    assert len(sample["text"]) > 100

def test_processed_file_exists():
    processed_path = os.path.join("socials_data", "personalities", "vitruvius", "processed", "data.jsonl")
    assert os.path.exists(processed_path)

    with open(processed_path, 'r') as f:
        lines = f.readlines()
        assert len(lines) > 0
        first_entry = json.loads(lines[0])
        assert "text" in first_entry
        assert "source" in first_entry
