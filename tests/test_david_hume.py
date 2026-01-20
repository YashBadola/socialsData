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
    assert len(sample["text"]) > 1000
    assert "sceptical" in sample["text"].lower() or "impression" in sample["text"].lower()
