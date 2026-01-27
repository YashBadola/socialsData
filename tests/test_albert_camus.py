import os
import pytest
from socials_data.core.loader import load_dataset

def test_load_albert_camus_dataset():
    """Test that the Albert Camus dataset can be loaded and contains valid data."""
    dataset = load_dataset("albert_camus")

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
        "the_myth_of_sisyphus.txt",
        "the_stranger.txt",
        "the_rebel.txt",
        "the_plague.txt"
    }

    # Verify all expected sources are present
    assert expected_sources.issubset(sources), f"Missing sources. Expected {expected_sources}, got {sources}"

    # Specific keywords we expect in Camus' text
    keywords = ["Sisyphus", "absurd", "rebel", "solidarity", "indifference", "plague"]
    found_keywords = set()
    for item in dataset:
        for keyword in keywords:
            if keyword in item["text"]:
                found_keywords.add(keyword)

    assert len(found_keywords) > 0, "Did not find any expected keywords in the dataset"

if __name__ == "__main__":
    test_load_albert_camus_dataset()
