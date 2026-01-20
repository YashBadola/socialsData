import os
import pytest
from socials_data.core.loader import load_dataset

def test_load_bertrand_russell_dataset():
    """Test that the Bertrand Russell dataset can be loaded and contains valid data."""
    dataset = load_dataset("bertrand_russell")

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
        "problems_of_philosophy.txt",
        "mysticism_and_logic.txt",
        "analysis_of_mind.txt",
        "proposed_roads_to_freedom.txt"
    }

    # Verify that the sources in the dataset are among the expected ones
    assert sources.issubset(expected_sources), f"Found unexpected sources: {sources - expected_sources}"

    # Also verify that we found all of them (since we know we processed 4 files)
    assert sources == expected_sources, f"Missing sources: {expected_sources - sources}"

    # Specific keywords we expect in Russell's text
    keywords = ["philosophy", "logic", "knowledge", "mind", "truth", "sensation"]
    found_keywords = False
    for item in dataset:
        for keyword in keywords:
            if keyword in item["text"]:
                found_keywords = True
                break
        if found_keywords:
            break

    assert found_keywords, "Did not find expected keywords in the dataset"

if __name__ == "__main__":
    test_load_bertrand_russell_dataset()
