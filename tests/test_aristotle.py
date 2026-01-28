import os
import pytest
from socials_data import load_dataset

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
    expected_sources = {
        "nicomachean_ethics.txt",
        "politics.txt",
        "poetics.txt",
        "metaphysics.txt"
    }

    # We check that at least these sources are present (if processing worked right, they should be)
    assert expected_sources.issubset(sources), f"Missing expected sources: {expected_sources - sources}"

    # Specific keywords we expect in Aristotle's text
    keywords = ["virtue", "political animal", "imitation", "being as being", "eudaimonia", "catharsis"]
    found_keywords = False

    # Check all items for keywords
    all_text = " ".join([item["text"].lower() for item in dataset])

    for keyword in keywords:
        if keyword in all_text:
            found_keywords = True
            break # Found at least one

    assert found_keywords, "Did not find expected keywords in the dataset"

    # Check for specific famous quotes/phrases we added
    assert "man is by nature a political animal" in all_text
    assert "every art and every inquiry" in all_text

if __name__ == "__main__":
    test_load_aristotle_dataset()
