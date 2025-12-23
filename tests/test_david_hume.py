
import pytest
from socials_data.core.loader import load_dataset
from socials_data.core.manager import PersonalityManager

def test_david_hume_dataset_loading():
    """Test that the David Hume dataset loads correctly."""
    dataset = load_dataset("david_hume")
    assert len(dataset) > 0, "Dataset should not be empty"

    # Check schema
    assert "text" in dataset.column_names, "Dataset should contain 'text' column"
    assert "source" in dataset.column_names, "Dataset should contain 'source' column"

def test_david_hume_content():
    """Test content of the David Hume dataset."""
    dataset = load_dataset("david_hume")

    # Check for expected keywords in the text
    keywords = ["experience", "reason", "passion", "impression", "idea", "moral", "understanding"]

    found_keywords = {k: False for k in keywords}

    # Check a sample of entries
    # dataset[:100] returns a dict of lists, so we iterate through the 'text' list
    for text in dataset[:100]["text"]:
        for k in keywords:
            if k in text.lower():
                found_keywords[k] = True

    # It's possible not all keywords are in the first 100 chunks, but most should be.
    # Let's assert at least some are found.
    assert found_keywords["experience"] or found_keywords["reason"], "Should find core Humean concepts"

def test_david_hume_metadata():
    """Test that metadata is correctly accessible."""
    manager = PersonalityManager()
    metadata = manager.get_metadata("david_hume")

    assert metadata["name"] == "David Hume"
    assert metadata["id"] == "david_hume"
    assert len(metadata["sources"]) == 3
