import pytest
import os
import json
from socials_data.core.loader import load_dataset
from socials_data.core.manager import PersonalityManager

def test_load_dataset_david_hume():
    """Test loading the David Hume dataset."""
    # Ensure the dataset exists
    manager = PersonalityManager()
    processed_path = manager.base_dir / "david_hume" / "processed" / "data.jsonl"
    if not processed_path.exists():
        pytest.skip("David Hume dataset not processed")

    # Load the dataset
    dataset = load_dataset("david_hume")

    # Check if it returns a dataset
    assert dataset is not None, "Dataset should not be None"

    # Check if it has data
    assert len(dataset) > 0, "Dataset should not be empty"

    # Check the first item
    item = dataset[0]
    assert "text" in item, "Item should contain 'text'"
    assert "source" in item, "Item should contain 'source'"

    # Check if text looks like Hume
    # Look for keywords that might appear in Hume's text
    # Note: 'text' might be a small chunk, so we scan a few items if needed

    found_hume_keyword = False
    keywords = ["reason", "passion", "impression", "idea", "cause", "effect", "human", "nature", "understanding", "sentiment"]

    for i in range(min(10, len(dataset))):
        text = dataset[i]["text"].lower()
        if any(keyword in text for keyword in keywords):
            found_hume_keyword = True
            break

    assert found_hume_keyword, "Should find common Humean keywords in the first few samples"

def test_metadata_david_hume():
    """Test metadata for David Hume."""
    manager = PersonalityManager()
    metadata = manager.get_metadata("david_hume")

    assert metadata["name"] == "David Hume"
    assert metadata["id"] == "david_hume"
    assert "system_prompt" in metadata
    assert "skeptic" in metadata["system_prompt"].lower()
    assert len(metadata["sources"]) == 2
