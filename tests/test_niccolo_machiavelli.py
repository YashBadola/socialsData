
import os
import json
import pytest
from socials_data.core.loader import load_dataset
from socials_data.core.manager import PersonalityManager

@pytest.fixture
def machiavelli_manager():
    return PersonalityManager()

def test_niccolo_machiavelli_exists(machiavelli_manager):
    personalities = machiavelli_manager.list_personalities()
    assert "niccolo_machiavelli" in personalities

def test_niccolo_machiavelli_metadata(machiavelli_manager):
    metadata = machiavelli_manager.get_metadata("niccolo_machiavelli")
    assert metadata["name"] == "Niccolò Machiavelli"
    assert metadata["id"] == "niccolo_machiavelli"
    assert "system_prompt" in metadata
    assert "The Prince" in [s["title"] for s in metadata["sources"]]
    assert "Discourses on the First Decade of Titus Livius" in [s["title"] for s in metadata["sources"]]

def test_load_niccolo_machiavelli_dataset():
    # Test loading the dataset
    ds = load_dataset("niccolo_machiavelli")

    # Check that we have data
    assert len(ds) > 0

    # Check sample content
    sample = ds[0]
    assert "text" in sample
    assert "source" in sample

    # Verify content relevance (checking for keywords)
    # Convert all text to lower case for searching
    all_text = "".join(ds["text"]).lower()

    keywords = ["prince", "republic", "virtue", "fortune", "italy", "florence"]
    for keyword in keywords:
        assert keyword in all_text, f"Keyword '{keyword}' not found in dataset"

def test_no_gutenberg_headers():
    # Load dataset manually to check for artifacts
    ds = load_dataset("niccolo_machiavelli")

    for item in ds:
        text = item["text"]
        # Basic checks for Project Gutenberg artifacts
        assert "*** START OF THE PROJECT" not in text
        assert "*** END OF THE PROJECT" not in text
        assert "Project Gutenberg License" not in text
