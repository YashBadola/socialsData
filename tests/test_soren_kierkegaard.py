import os
import pytest
from socials_data.core.loader import load_dataset

def test_load_kierkegaard_dataset():
    """Test that the Soren Kierkegaard dataset can be loaded and contains valid data."""
    dataset = load_dataset("soren_kierkegaard")

    # Check if dataset is not empty
    assert len(dataset) > 0, "Dataset should not be empty"
    # We added 3 files
    assert len(dataset) == 3

    # Check the structure of the first item
    first_item = dataset[0]
    assert "text" in first_item, "Item should contain 'text' field"
    assert "source" in first_item, "Item should contain 'source' field"

    # Check sources
    sources = set(item["source"] for item in dataset)
    expected_sources = {"fear_and_trembling.txt", "sickness_unto_death.txt", "either_or.txt"}
    assert sources == expected_sources, f"Expected sources {expected_sources}, but got {sources}"

    # Specific keywords
    keywords = ["anxiety", "despair", "faith", "Abraham"]
    found_keywords = False
    for item in dataset:
        for keyword in keywords:
            if keyword in item["text"]:
                found_keywords = True
                break
        if found_keywords:
            break

    assert found_keywords, "Did not find expected keywords in the dataset"
