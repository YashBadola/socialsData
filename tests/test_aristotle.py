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
    expected_sources = {"nicomachean_ethics.txt", "politics.txt", "metaphysics.txt", "poetics.txt"}

    # We expect all sources to be present since we added them
    assert sources.issubset(expected_sources), f"Found unexpected sources: {sources - expected_sources}"
    assert expected_sources.issubset(sources), f"Missing sources: {expected_sources - sources}"

    # Specific keywords we expect in Aristotle's text
    keywords = ["virtue", "political", "wisdom", "tragedy", "state"]
    found_keywords = {k: False for k in keywords}

    for item in dataset:
        for keyword in keywords:
            if keyword in item["text"].lower():
                found_keywords[keyword] = True

    for keyword, found in found_keywords.items():
        assert found, f"Did not find expected keyword '{keyword}' in the dataset"

if __name__ == "__main__":
    test_load_aristotle_dataset()
