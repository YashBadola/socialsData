import os
import pytest
from socials_data.core.loader import load_dataset

def test_load_wittgenstein_dataset():
    """Test that the Ludwig Wittgenstein dataset can be loaded and contains valid data."""
    dataset = load_dataset("ludwig_wittgenstein")

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
    expected_sources = {"tractatus_excerpts.txt", "philosophical_investigations_excerpts.txt"}

    # Check that the sources present are valid.
    assert sources.issubset(expected_sources), f"Found unexpected sources: {sources - expected_sources}"
    assert len(sources) == 2, "Should have data from both source files"

    # Specific keywords we expect in Wittgenstein's text
    keywords = ["language-game", "beetle", "atomic fact", "logical space", "Whereof one cannot speak"]
    found_keywords = 0
    for item in dataset:
        for keyword in keywords:
            if keyword in item["text"]:
                found_keywords += 1

    assert found_keywords > 0, "Did not find expected keywords in the dataset"

if __name__ == "__main__":
    test_load_wittgenstein_dataset()
