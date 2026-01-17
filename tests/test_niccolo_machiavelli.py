import pytest
from socials_data.core.manager import PersonalityManager
import os
import json
from socials_data import load_dataset

def test_niccolo_machiavelli_exists():
    manager = PersonalityManager()
    personalities = manager.list_personalities()
    assert "niccolo_machiavelli" in personalities

def test_niccolo_machiavelli_metadata():
    manager = PersonalityManager()
    metadata = manager.get_metadata("niccolo_machiavelli")
    assert metadata["name"] == "Niccolò Machiavelli"
    assert metadata["id"] == "niccolo_machiavelli"
    titles = [s["title"] for s in metadata["sources"]]
    assert "The Prince" in titles
    assert "Discourses on the First Decade of Titus Livius" in titles

def test_niccolo_machiavelli_data_loaded():
    dataset = load_dataset("niccolo_machiavelli")
    # We expect 2 entries, one for each book
    assert len(dataset) == 2

    # Check sample structure
    # Since we have 2 entries, let's check both sources are present
    sources = set(d["source"] for d in dataset)
    assert "the_prince.txt" in sources
    assert "discourses_on_livy.txt" in sources

    for sample in dataset:
        assert isinstance(sample["text"], str)
        assert len(sample["text"]) > 100

def test_processed_file_exists():
    processed_path = os.path.join("socials_data", "personalities", "niccolo_machiavelli", "processed", "data.jsonl")
    assert os.path.exists(processed_path)

    with open(processed_path, 'r') as f:
        lines = f.readlines()
        assert len(lines) == 2
        first_entry = json.loads(lines[0])
        assert "text" in first_entry
        assert "source" in first_entry
