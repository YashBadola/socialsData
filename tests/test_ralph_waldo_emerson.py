import os
import pytest
from socials_data.core.loader import load_dataset
from socials_data.core.manager import PersonalityManager

def test_load_emerson_dataset():
    """Test that the Ralph Waldo Emerson dataset loads correctly."""
    dataset = load_dataset("ralph_waldo_emerson")

    assert len(dataset) > 0, "Dataset should not be empty"

    # Check first item
    first_item = dataset[0]
    assert "text" in first_item
    assert "source" in first_item
    assert isinstance(first_item["text"], str)

    # Check random sample for key themes
    texts = [item["text"] for item in dataset]
    combined_text = " ".join(texts)

    # These words should definitely appear in Emerson's works
    keywords = ["self-reliance", "nature", "soul", "mind", "man", "truth"]
    for keyword in keywords:
        assert keyword in combined_text.lower(), f"Keyword '{keyword}' not found in dataset"

def test_emerson_metadata():
    """Test that metadata is correctly configured."""
    manager = PersonalityManager()
    metadata = manager.get_metadata("ralph_waldo_emerson")

    assert metadata["name"] == "Ralph Waldo Emerson"
    assert len(metadata["sources"]) == 5
    assert "Transcendentalist" in metadata["system_prompt"]
    assert "self-reliance" in metadata["system_prompt"]

def test_no_gutenberg_headers():
    """Test that Project Gutenberg headers are removed."""
    dataset = load_dataset("ralph_waldo_emerson")
    texts = [item["text"] for item in dataset]
    combined_text = " ".join(texts)

    # Check for various footer/header artifacts
    artifacts = [
        "*** START OF THE PROJECT GUTENBERG",
        "End of the Project Gutenberg",
        "End of Project Gutenberg",
        "PROJECT GUTENBERG EBOOK",
        "Project Gutenberg License"
    ]

    for artifact in artifacts:
        assert artifact not in combined_text, f"Found artifact: {artifact}"
