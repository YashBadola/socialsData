import os
import pytest
from socials_data.core.loader import load_dataset

def test_load_ludwig_dataset():
    """Test that the Ludwig Wittgenstein dataset can be loaded and contains valid data."""
    dataset = load_dataset("ludwig_wittgenstein")

    # Check if dataset is not empty
    assert len(dataset) > 0, "Dataset should not be empty"
    # We expect 8 items (Preface + 7 Props)
    assert len(dataset) == 8, f"Expected 8 items, found {len(dataset)}"

    # Check the structure of the first item
    first_item = dataset[0]
    assert "text" in first_item, "Item should contain 'text' field"
    assert "source" in first_item, "Item should contain 'source' field"

    # Check sources
    sources = set(item["source"] for item in dataset)
    expected_sources = {
        "preface.txt",
        "prop_1.txt", "prop_2.txt", "prop_3.txt",
        "prop_4.txt", "prop_5.txt", "prop_6.txt", "prop_7.txt"
    }

    assert sources == expected_sources, f"Sources mismatch. Found: {sources}, Expected: {expected_sources}"

    # Specific keywords we expect in Ludwig's text
    keywords = ["world", "logic", "proposition", "fact", "silence"]
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
    test_load_ludwig_dataset()
