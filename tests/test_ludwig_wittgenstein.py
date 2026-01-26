import os
import pytest
from socials_data.core.loader import load_dataset

def test_load_ludwig_wittgenstein_dataset():
    """Test that the Ludwig Wittgenstein dataset can be loaded and contains valid data."""
    dataset = load_dataset("ludwig_wittgenstein")

    # Check if dataset is not empty
    assert len(dataset) > 0, "Dataset should not be empty"

    # Check the structure of the first item
    first_item = dataset[0]
    assert "text" in first_item, "Item should contain 'text' field"
    assert "source" in first_item, "Item should contain 'source' field"

    # Check sources
    sources = set(item["source"] for item in dataset)
    expected_sources = {"tractatus.txt", "philosophical_investigations.txt"}

    assert sources == expected_sources, f"Found unexpected or missing sources: {sources}"

    # Specific keywords we expect
    keywords = ["language-game", "silent", "meaning", "world"]
    found_keywords = set()
    for item in dataset:
        for keyword in keywords:
            if keyword in item["text"]:
                found_keywords.add(keyword)

    assert len(found_keywords) > 0, f"Did not find enough keywords. Found: {found_keywords}"

if __name__ == "__main__":
    test_load_ludwig_wittgenstein_dataset()
