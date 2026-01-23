import os
import pytest
from socials_data.core.loader import load_dataset

def test_load_heraclitus_dataset():
    """Test that the Heraclitus dataset can be loaded and contains valid data."""
    dataset = load_dataset("heraclitus")

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
        "flux.txt",
        "logos.txt",
        "opposites.txt",
        "cosmos.txt",
        "critiques.txt",
        "life_and_death.txt"
    }

    assert sources.issubset(expected_sources), f"Found unexpected sources: {sources - expected_sources}"
    assert expected_sources.issubset(sources), f"Missing expected sources: {expected_sources - sources}"

    # Specific keywords we expect in Heraclitus's text
    keywords = ["river", "fire", "reason", "change", "harmony", "war", "sleep"]
    found_keywords = set()
    for item in dataset:
        for keyword in keywords:
            if keyword.lower() in item["text"].lower():
                found_keywords.add(keyword)

    missing_keywords = set(keywords) - found_keywords
    assert not missing_keywords, f"Did not find expected keywords in the dataset: {missing_keywords}"

if __name__ == "__main__":
    test_load_heraclitus_dataset()
