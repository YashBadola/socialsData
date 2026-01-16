import pytest
from socials_data.core.manager import PersonalityManager
from socials_data import load_dataset
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
    assert any("Enquiry" in s["title"] for s in metadata["sources"])

def test_david_hume_data_loaded():
    dataset = load_dataset("david_hume")
    assert len(dataset) > 0

    # Check sample structure
    sample = dataset[0]
    assert "text" in sample
    assert "source" in sample
    assert sample["source"] == "enquiry.txt"

    # Check for keywords from "Enquiry"
    # The text is likely split into chunks or is one big chunk depending on processor logic.
    # We'll check if text is a string and has reasonable length.
    assert isinstance(sample["text"], str)
    assert len(sample["text"]) > 100

    # Check for some specific text that should be in the book
    combined_text = " ".join([d["text"] for d in dataset])
    assert "cause and effect" in combined_text or "Cause and Effect" in combined_text or "CAUSE AND EFFECT" in combined_text
    assert "experience" in combined_text
