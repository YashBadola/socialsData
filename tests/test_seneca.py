import os
import pytest
from socials_data import load_dataset
from socials_data.core.manager import PersonalityManager

def test_load_dataset_seneca():
    """Test loading the Seneca dataset."""
    dataset = load_dataset("seneca")
    assert dataset is not None, "Dataset should not be None"
    assert len(dataset) > 0, "Dataset should not be empty"

    # Check the schema
    sample = dataset[0]
    assert "text" in sample
    assert isinstance(sample["text"], str)
    assert len(sample["text"]) > 0

    # Basic content check
    # We expect some words related to Seneca or Stoicism
    keywords = ["virtue", "reason", "nature", "happy", "benefit", "good", "evil", "mind", "life"]

    # Check if any keyword appears in the first few samples
    found_keyword = False
    for i in range(min(len(dataset), 20)):
        text = dataset[i]["text"].lower()
        if any(k in text for k in keywords):
            found_keyword = True
            break

    assert found_keyword, "Dataset should contain relevant keywords"

def test_metadata_seneca():
    """Test Seneca metadata."""
    manager = PersonalityManager()
    metadata = manager.get_metadata("seneca")

    assert metadata["name"] == "Seneca"
    assert metadata["id"] == "seneca"
    assert "system_prompt" in metadata
    assert len(metadata["sources"]) > 0
