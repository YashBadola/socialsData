import os
import pytest
from socials_data.core.loader import load_dataset
from socials_data.core.manager import PersonalityManager

def test_load_rousseau_dataset():
    """Test that the Jean-Jacques Rousseau dataset loads correctly."""
    dataset = load_dataset("jean_jacques_rousseau")

    # Check if dataset is not empty
    assert len(dataset) > 0, "Dataset should not be empty"

    # Check structure
    sample = dataset[0]
    assert "text" in sample, "Dataset should have a 'text' column"
    assert "source" in sample, "Dataset should have a 'source' column"

    # Check content (verify we have some known text from Rousseau)
    # We load all text to check for keywords
    all_text = " ".join([item["text"] for item in dataset])

    # Social Contract keywords
    assert "Social Contract" in all_text or "Man is born free" in all_text or "general will" in all_text

    # Emile keywords
    assert "Emile" in all_text or "education" in all_text

    # Confessions keywords
    assert "Confessions" in all_text or "Jean-Jacques" in all_text

def test_metadata():
    """Test metadata for Jean-Jacques Rousseau."""
    manager = PersonalityManager()
    metadata = manager.get_metadata("jean_jacques_rousseau")

    assert metadata["name"] == "Jean-Jacques Rousseau"
    assert len(metadata["sources"]) == 3
    assert metadata["sources"][0]["title"] == "The Social Contract & Discourses"
