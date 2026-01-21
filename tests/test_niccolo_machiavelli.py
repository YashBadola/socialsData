import os
import pytest
from socials_data.core.loader import load_dataset

def test_load_machiavelli_dataset():
    """Test that the Machiavelli dataset can be loaded and contains valid data."""
    dataset = load_dataset("niccolo_machiavelli")

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
    expected_sources = {"the_prince.txt", "life_of_castruccio.txt"}

    assert sources.issubset(expected_sources), f"Found unexpected sources: {sources - expected_sources}"
    assert "the_prince.txt" in sources
    assert "life_of_castruccio.txt" in sources

    # Specific keywords we expect in Machiavelli's text
    keywords = ["Prince", "virtue", "fortune", "state", "arms"]
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
    test_load_machiavelli_dataset()
