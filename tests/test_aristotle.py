import os
import pytest
from socials_data.core.loader import load_dataset

def test_load_aristotle_dataset():
    """Test that the Aristotle dataset can be loaded and contains valid data."""
    dataset = load_dataset("aristotle")

    # Check if dataset is not empty
    assert len(dataset) > 0, "Dataset should not be empty"

    # Check the structure of the first item
    first_item = dataset[0]
    assert "text" in first_item, "Item should contain 'text' field"
    assert "source" in first_item, "Item should contain 'source' field"

    # Check content of the text
    text = first_item["text"]
    assert isinstance(text, str), "Text should be a string"
    assert len(text) > 0, "Text should not be empty"

    # Check sources
    sources = set(item["source"] for item in dataset)
    expected_sources = {"nicomachean_ethics.txt", "politics.txt"}

    # We expect both sources to be present since we processed both.
    # Note: load_dataset might return a dataset object where we need to iterate to see all sources.
    # If the dataset is large, this might be slow, but here we only have 2 files (2 lines in jsonl if not chunked further).
    # The TextDataProcessor currently returns "whole cleaned text as one chunk" per file.
    # So we expect exactly 2 items.

    assert len(dataset) == 2, f"Expected 2 items, found {len(dataset)}"
    assert sources == expected_sources, f"Expected sources {expected_sources}, found {sources}"

    # Specific keywords we expect in Aristotle's text
    keywords = ["virtue", "happiness", "state", "citizen", "mean", "ethics", "political"]
    found_keywords = False
    for item in dataset:
        for keyword in keywords:
            if keyword in item["text"].lower():
                found_keywords = True
                break
        if found_keywords:
            break

    assert found_keywords, "Did not find expected keywords in the dataset"

if __name__ == "__main__":
    test_load_aristotle_dataset()
