import pytest
from socials_data.core.manager import PersonalityManager
import os
import json

def test_david_hume_exists():
    manager = PersonalityManager()
    personalities = manager.list_personalities()
    assert "david_hume" in personalities

def test_david_hume_metadata():
    manager = PersonalityManager()
    metadata = manager.get_metadata("david_hume")
    assert metadata["name"] == "David Hume"
    assert metadata["id"] == "david_hume"
    assert "An Enquiry Concerning Human Understanding" in [s["title"] for s in metadata["sources"]]
    assert metadata["system_prompt"] is not None

def test_david_hume_data_loaded():
    from socials_data import load_dataset
    dataset = load_dataset("david_hume")
    assert len(dataset) > 0

    # Check sample structure
    sample = dataset[0]
    assert "text" in sample
    assert "source" in sample
    assert sample["source"] == "enquiry.txt"

    # Check for content
    assert isinstance(sample["text"], str)
    # Check for a phrase that definitely appears in Hume's Enquiry
    assert "cause and effect" in sample["text"] or "impression" in sample["text"]

def test_processed_file_exists():
    processed_path = os.path.join("socials_data", "personalities", "david_hume", "processed", "data.jsonl")
    assert os.path.exists(processed_path)

    with open(processed_path, 'r') as f:
        lines = f.readlines()
        assert len(lines) > 0
        first_entry = json.loads(lines[0])
        assert "text" in first_entry
        assert "source" in first_entry
