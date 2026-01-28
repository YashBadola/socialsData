import pytest
from socials_data.core.manager import PersonalityManager
import os
import json

def test_jean_paul_sartre_exists():
    manager = PersonalityManager()
    personalities = manager.list_personalities()
    assert "jean_paul_sartre" in personalities

def test_jean_paul_sartre_metadata():
    manager = PersonalityManager()
    metadata = manager.get_metadata("jean_paul_sartre")
    assert metadata["name"] == "Jean-Paul Sartre"
    assert metadata["id"] == "jean_paul_sartre"
    titles = [s["title"] for s in metadata["sources"]]
    assert "Existentialism is a Humanism" in titles
    assert "Nausea" in titles

def test_jean_paul_sartre_data_loaded():
    from socials_data import load_dataset
    dataset = load_dataset("jean_paul_sartre")
    # We added 2 files
    assert len(dataset) == 2

    # Check sample structure
    sample = dataset[0]
    assert "text" in sample
    assert "source" in sample

    # Check sources presence
    sources = set(item["source"] for item in dataset)
    assert "existentialism_is_a_humanism.txt" in sources
    assert "nausea_excerpts.txt" in sources

    # Check content
    all_text = " ".join([item["text"] for item in dataset])
    assert "existence precedes essence" in all_text
    assert "The roots of the chestnut tree" in all_text

def test_processed_file_exists():
    processed_path = os.path.join("socials_data", "personalities", "jean_paul_sartre", "processed", "data.jsonl")
    assert os.path.exists(processed_path)

    with open(processed_path, 'r') as f:
        lines = f.readlines()
        assert len(lines) == 2
        first_entry = json.loads(lines[0])
        assert "text" in first_entry
        assert "source" in first_entry
