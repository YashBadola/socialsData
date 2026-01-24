import os
import pytest
from socials_data.core.loader import load_dataset

def test_load_michel_foucault_dataset():
    """Test that the Michel Foucault dataset can be loaded and contains valid data."""
    dataset = load_dataset("michel_foucault")

    # Check if dataset is not empty
    assert len(dataset) > 0, "Dataset should not be empty"
    # We expect 3 items corresponding to the 3 files
    assert len(dataset) == 3, "Dataset should contain 3 items"

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
    expected_sources = {"panopticism.txt", "power_knowledge.txt", "biopolitics.txt"}

    assert sources == expected_sources, f"Sources mismatch. Found: {sources}, Expected: {expected_sources}"

    # Specific keywords we expect
    keywords = ["Panopticon", "power", "knowledge", "biopolitics", "sexuality", "discipline"]
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
    test_load_michel_foucault_dataset()
