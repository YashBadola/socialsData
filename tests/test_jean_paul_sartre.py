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
    assert "Existentialism is a Humanism" in [s["title"] for s in metadata["sources"]]

def test_jean_paul_sartre_data_loaded():
    from socials_data import load_dataset
    dataset = load_dataset("jean_paul_sartre")
    assert len(dataset) > 0

    # Check sample structure
    sample = dataset[0]
    assert "text" in sample
    assert "source" in sample
    assert sample["source"] == "existentialism_is_a_humanism.txt"

    # Check content
    assert isinstance(sample["text"], str)
    assert len(sample["text"]) > 100
    # "existentialism" should definitely be in there
    text_content = " ".join([d["text"] for d in dataset]).lower()
    assert "existentialism" in text_content
    assert "humanism" in text_content

def test_processed_file_exists():
    processed_path = os.path.join("socials_data", "personalities", "jean_paul_sartre", "processed", "data.jsonl")
    assert os.path.exists(processed_path)

    with open(processed_path, 'r') as f:
        lines = f.readlines()
        assert len(lines) > 0
        first_entry = json.loads(lines[0])
        assert "text" in first_entry
        assert "source" in first_entry
