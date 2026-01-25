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
    # Check that sources list contains "Ethics"
    assert any("Ethics" in s["title"] for s in metadata["sources"])

def test_baruch_spinoza_data_loaded():
    from socials_data import load_dataset
    dataset = load_dataset("baruch_spinoza")
    assert len(dataset) == 5

    # Gather all text to check for key concepts
    all_text = " ".join([item["text"] for item in dataset])

    assert "Substance" in all_text
    assert "God" in all_text
    assert "mode" in all_text
    assert "intellectual love of God" in all_text

def test_processed_file_exists():
    processed_path = os.path.join("socials_data", "personalities", "baruch_spinoza", "processed", "data.jsonl")
    assert os.path.exists(processed_path)

    with open(processed_path, 'r') as f:
        lines = f.readlines()
        assert len(lines) == 5
        for line in lines:
            entry = json.loads(line)
            assert "text" in entry
            assert "source" in entry
