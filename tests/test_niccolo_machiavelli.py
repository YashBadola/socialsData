import pytest
from socials_data.core.loader import load_dataset
from socials_data.core.manager import PersonalityManager
import os
from pathlib import Path

def test_load_machiavelli_dataset():
    """Test that the Machiavelli dataset loads correctly."""
    dataset = load_dataset("niccolo_machiavelli")
    assert dataset is not None, "Dataset should not be None"
    assert len(dataset) > 0, "Dataset should have entries"

    # Check structure
    sample = dataset[0]
    assert "text" in sample, "Sample should contain 'text'"
    assert "source" in sample, "Sample should contain 'source'"

    # Check content relevance (basic check)
    # Just checking if we have enough text to likely include common words
    all_text = " ".join([d["text"] for d in dataset])
    assert "prince" in all_text.lower(), "Text should contain 'prince'"
    assert "state" in all_text.lower(), "Text should contain 'state'"

def test_machiavelli_metadata():
    """Test that metadata is correctly accessible."""
    manager = PersonalityManager()
    metadata = manager.get_metadata("niccolo_machiavelli")

    assert metadata["name"] == "Niccolo Machiavelli"
    assert metadata["id"] == "niccolo_machiavelli"
    assert "system_prompt" in metadata
    assert len(metadata["sources"]) > 0
    assert metadata["sources"][0]["title"] == "The Prince"
