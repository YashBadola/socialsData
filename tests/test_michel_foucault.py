import os
import pytest
from socials_data.core.loader import load_dataset

def test_load_foucault_dataset():
    """Test that the Michel Foucault dataset can be loaded and contains valid data."""
    dataset = load_dataset("michel_foucault")

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
    expected_sources = {"panopticism.txt", "history_of_sexuality.txt", "power_knowledge.txt"}

    # Check that expected sources are present in the dataset
    assert expected_sources.issubset(sources), f"Missing expected sources: {expected_sources - sources}"

    # Specific keywords we expect in Foucault's text
    keywords = ["Panopticon", "power", "discipline", "sexuality", "knowledge"]
    found_keywords = {keyword: False for keyword in keywords}

    for item in dataset:
        for keyword in keywords:
            if keyword in item["text"]:
                found_keywords[keyword] = True

        if all(found_keywords.values()):
            break

    # Check which keywords were not found
    missing_keywords = [k for k, v in found_keywords.items() if not v]
    assert not missing_keywords, f"Did not find expected keywords: {missing_keywords}"

if __name__ == "__main__":
    test_load_foucault_dataset()
