
import pytest
import os
from socials_data.core.loader import load_dataset
from socials_data.core.manager import PersonalityManager

def test_load_plato_dataset():
    """Test loading the Plato dataset."""
    try:
        dataset = load_dataset("plato")
    except ValueError as e:
        pytest.fail(f"Failed to load dataset: {e}")

    # Check that it returns a Dataset object (or list of dicts depending on implementation,
    # but memory says 'load_dataset returns a Hugging Face Dataset object')
    # However, since I installed `datasets`, it should be a Dataset object.

    assert len(dataset) > 0, "Dataset should not be empty"

    # Check first item schema
    item = dataset[0]
    assert "text" in item
    assert "source" in item
    assert isinstance(item["text"], str)
    assert isinstance(item["source"], str)

def test_plato_content():
    """Test that the dataset contains expected Plato content."""
    dataset = load_dataset("plato")

    # Search for a known phrase from Apology or Republic
    found_socrates = False
    found_republic_keyword = False # e.g. "justice" or "Glaucon"

    for item in dataset:
        text = item["text"]
        if "Socrates" in text:
            found_socrates = True
        if "justice" in text or "Glaucon" in text:
            found_republic_keyword = True

        if found_socrates and found_republic_keyword:
            break

    assert found_socrates, "Should contain 'Socrates'"
    assert found_republic_keyword, "Should contain keywords like 'justice' or 'Glaucon'"

def test_plato_metadata():
    """Test retrieving Plato metadata."""
    manager = PersonalityManager()
    metadata = manager.get_metadata("plato")

    assert metadata["name"] == "Plato"
    assert metadata["id"] == "plato"
    assert len(metadata["sources"]) == 3
