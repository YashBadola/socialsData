import os
import pytest
from socials_data.core.loader import load_dataset

def test_load_hannah_arendt_dataset():
    """Test that the Hannah Arendt dataset can be loaded and contains valid data."""
    dataset = load_dataset("hannah_arendt")

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
        "the_human_condition_excerpts.txt",
        "origins_of_totalitarianism_notes.txt",
        "banality_of_evil_reflections.txt"
    }

    assert sources.issubset(expected_sources), f"Found unexpected sources: {sources - expected_sources}"
    assert len(sources) == len(expected_sources), "Not all expected sources were found in the dataset"

    # Specific keywords we expect in Arendt's text
    keywords = ["totalitarianism", "plurality", "banality", "Eichmann", "public realm", "labor", "work", "action"]

    for keyword in keywords:
        found = False
        for item in dataset:
            if keyword.lower() in item["text"].lower():
                found = True
                break
        assert found, f"Did not find expected keyword '{keyword}' in the dataset"

if __name__ == "__main__":
    test_load_hannah_arendt_dataset()
