import os
import pytest
from socials_data import load_dataset

def test_load_dataset_immanuel_kant():
    """Test loading the immanuel_kant dataset."""
    dataset = load_dataset("immanuel_kant")

    assert dataset is not None, "Dataset should not be None"
    # Check if we have rows
    assert len(dataset) > 0, "Dataset should not be empty"

    # Check the first item structure
    first_item = dataset[0]
    assert "text" in first_item, "Item should have 'text' field"
    assert "source" in first_item, "Item should have 'source' field"

    # Check content relevance (sample check)
    # We might not find these exact words in the *first* chunk, but let's check if *some* item has them
    # or just check that the text is non-empty string.
    assert isinstance(first_item["text"], str)
    assert len(first_item["text"]) > 0

    # Verify source is correct
    assert first_item["source"] == "critique_of_pure_reason.txt"

    # Search for a known phrase in the first few items to verify content
    found_phrase = False
    for i in range(min(10, len(dataset))):
        text = dataset[i]["text"]
        if "reason" in text.lower() or "critique" in text.lower() or "concept" in text.lower():
            found_phrase = True
            break

    assert found_phrase, "Did not find expected keywords in the first few chunks"
