import os
import pytest
from socials_data import load_dataset
from socials_data.core.manager import PersonalityManager

def test_immanuel_kant_exists():
    """Test that Immanuel Kant exists in the registry."""
    manager = PersonalityManager()
    personalities = manager.list_personalities()
    assert "immanuel_kant" in personalities

def test_immanuel_kant_metadata():
    """Test that metadata for Immanuel Kant is correct."""
    manager = PersonalityManager()
    metadata = manager.get_metadata("immanuel_kant")
    assert metadata["name"] == "Immanuel Kant"
    assert metadata["id"] == "immanuel_kant"
    assert "transcendental idealist" in metadata["system_prompt"]
    assert len(metadata["sources"]) == 5

def test_load_dataset():
    """Test loading the dataset."""
    dataset = load_dataset("immanuel_kant")
    assert len(dataset) > 0
    # Check for expected content
    sample_text = dataset[0]["text"]
    assert isinstance(sample_text, str)
    assert len(sample_text) > 0

    # Check if we can find some Kantian keywords in the dataset (scanning a few samples)
    found_keyword = False
    keywords = ["reason", "transcendental", "imperative", "critique", "judgment", "judgement", "pure", "practical"]

    for i in range(min(5, len(dataset))):
        text = dataset[i]["text"].lower()
        if any(k in text for k in keywords):
            found_keyword = True
            break

    assert found_keyword, "Did not find expected Kantian keywords in the first few samples"

def test_no_gutenberg_headers():
    """Test that Gutenberg headers are stripped."""
    dataset = load_dataset("immanuel_kant")
    for i in range(min(10, len(dataset))):
        text = dataset[i]["text"]
        assert "*** START OF THE PROJECT GUTENBERG EBOOK" not in text
        assert "*** END OF THE PROJECT GUTENBERG EBOOK" not in text
        assert "Project Gutenberg" not in text # Tighter check, might fail if license is somewhere else, but let's try
