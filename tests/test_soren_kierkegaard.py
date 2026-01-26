import os
import pytest
from socials_data import load_dataset

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
    expected_sources = {"fear_and_trembling_excerpt.txt", "sickness_unto_death_excerpt.txt"}

    # Check that our expected sources are present
    assert sources.issubset(expected_sources), f"Found unexpected sources: {sources - expected_sources}"
    assert len(sources) == 2, f"Expected 2 sources, found {len(sources)}"

    # Specific keywords we expect in Kierkegaard's text
    keywords = ["Knight of Faith", "despair", "absurd", "synthesis"]
    found_keywords = 0
    for item in dataset:
        for keyword in keywords:
            if keyword in item["text"]:
                found_keywords += 1

    assert found_keywords > 0, "Did not find expected keywords in the dataset"

if __name__ == "__main__":
    test_load_kierkegaard_dataset()
