import os
import pytest
from socials_data.core.loader import load_dataset

def test_load_kierkegaard_dataset():
    """Test that the Soren Kierkegaard dataset can be loaded and contains valid data."""
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
    expected_sources = {"either_or.txt", "fear_and_trembling.txt", "sickness_unto_death.txt", "philosophical_fragments.txt"}

    assert sources.issubset(expected_sources), f"Found unexpected sources: {sources - expected_sources}"

    # Specific keywords we expect in Kierkegaard's text
    keywords = ["anxiety", "faith", "subjectivity", "paradox", "aesthetic", "ethical", "despair"]
    found_keywords = False
    for item in dataset:
        for keyword in keywords:
            if keyword in item["text"].lower(): # simple case insensitive check
                found_keywords = True
                break
        if found_keywords:
            break

    assert found_keywords, "Did not find expected keywords in the dataset"

if __name__ == "__main__":
    test_load_kierkegaard_dataset()
