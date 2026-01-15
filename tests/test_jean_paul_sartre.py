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
    assert "Being and Nothingness" in [s["title"] for s in metadata["sources"]]

def test_processed_file_exists():
    processed_path = os.path.join("socials_data", "personalities", "jean_paul_sartre", "processed", "data.jsonl")
    assert os.path.exists(processed_path)

    with open(processed_path, 'r') as f:
        lines = f.readlines()
        assert len(lines) > 0
        first_entry = json.loads(lines[0])
        assert "text" in first_entry
        assert "source" in first_entry
