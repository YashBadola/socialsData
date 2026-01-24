import os
import pytest
from socials_data.core.loader import load_dataset

def test_load_kierkegaard_dataset():
    """Test that the Kierkegaard dataset can be loaded and contains valid data."""
    dataset = load_dataset("soren_kierkegaard")

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
    expected_sources = {"fear_and_trembling_excerpts.txt", "either_or_excerpts.txt"}

    # We expect these sources to be present
    assert sources.issubset(expected_sources), f"Found unexpected sources: {sources - expected_sources}"
    assert len(sources) == len(expected_sources), f"Missing sources: {expected_sources - sources}"

    # Specific keywords we expect in Kierkegaard's text
    keywords = ["Abraham", "dread", "aesthetic", "ethical", "paradox", "Isaac"]
    found_keywords = {k: False for k in keywords}

    for item in dataset:
        for keyword in keywords:
            if keyword in item["text"]:
                found_keywords[keyword] = True

    # Check if we found all keywords (since our excerpts are small and focused, we expect all of them)
    not_found = [k for k, v in found_keywords.items() if not v]
    assert not not_found, f"Did not find expected keywords in the dataset: {not_found}"

if __name__ == "__main__":
    test_load_kierkegaard_dataset()
