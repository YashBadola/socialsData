import pytest
from socials_data.core.loader import load_dataset
from pathlib import Path
import json

def test_aristotle_dataset_loading():
    """Test that the Aristotle dataset loads correctly."""
    dataset = load_dataset("aristotle")
    assert dataset is not None, "Dataset should not be None"
    assert len(dataset) > 0, "Dataset should not be empty"

    # Check structure of the first item
    first_item = dataset[0]
    assert "text" in first_item
    assert "source" in first_item
    assert isinstance(first_item["text"], str)
    assert isinstance(first_item["source"], str)

def test_aristotle_content_check():
    """Check for specific keywords expected in Aristotle's works."""
    dataset = load_dataset("aristotle")

    # We expect words like "virtue", "happiness", "state", "tragedy"
    keywords = ["virtue", "happiness", "state", "tragedy"]
    found_keywords = {k: False for k in keywords}

    # Scan a subset of the dataset to be fast
    for item in dataset:
        text = item["text"].lower()
        for k in keywords:
            if k in text:
                found_keywords[k] = True

        if all(found_keywords.values()):
            break

    assert all(found_keywords.values()), f"Missing keywords: {[k for k, v in found_keywords.items() if not v]}"

def test_metadata_integrity():
    """Verify metadata.json exists and has correct fields."""
    metadata_path = Path("socials_data/personalities/aristotle/metadata.json")
    assert metadata_path.exists()

    with open(metadata_path, 'r') as f:
        metadata = json.load(f)

    assert metadata["id"] == "aristotle"
    assert "system_prompt" in metadata
    assert len(metadata["sources"]) == 3
