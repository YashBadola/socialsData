import os
import pytest
from socials_data import load_dataset

def test_load_dataset_david_hume():
    """Test loading the David Hume dataset."""
    dataset = load_dataset("david_hume")
    assert dataset is not None, "Dataset should not be None"

    # Check if we have data
    assert len(dataset) > 0, "Dataset should not be empty"

    # Check the schema of the first item
    first_item = dataset[0]
    assert "text" in first_item, "Item should have 'text' field"
    assert "source" in first_item, "Item should have 'source' field"

    # Check for specific keywords related to Hume
    # Iterate through a few items to find keywords since the text is chunked
    found_keyword = False
    keywords = ["impression", "idea", "skepticism", "reason", "passion", "human", "nature", "mind"]

    for i in range(min(100, len(dataset))):
        text = dataset[i]["text"].lower()
        if any(k in text for k in keywords):
            found_keyword = True
            break

    assert found_keyword, "Should find Hume-related keywords in the first 100 chunks"

def test_metadata_structure():
    """Test the metadata file structure."""
    import json
    from pathlib import Path

    metadata_path = Path("socials_data/personalities/david_hume/metadata.json")
    assert metadata_path.exists(), "Metadata file should exist"

    with open(metadata_path, "r") as f:
        metadata = json.load(f)

    assert metadata["id"] == "david_hume"
    assert "system_prompt" in metadata
    assert "sources" in metadata
    assert len(metadata["sources"]) == 3
