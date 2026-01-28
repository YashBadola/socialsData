import pytest
from socials_data.core.loader import load_dataset

def test_load_kierkegaard_dataset():
    """Test that the Søren Kierkegaard dataset can be loaded and contains valid data."""
    dataset = load_dataset("soren_kierkegaard")

    # Check if dataset is not empty
    assert len(dataset) > 0, "Dataset should not be empty"

    # Check length (we know we added 2 files, so we expect 2 items)
    assert len(dataset) == 2, f"Expected 2 items, found {len(dataset)}"

    # Check the structure of the first item
    first_item = dataset[0]
    assert "text" in first_item, "Item should contain 'text' field"
    assert "source" in first_item, "Item should contain 'source' field"

    # Check sources
    sources = set(item["source"] for item in dataset)
    expected_sources = {"fear_and_trembling.txt", "sickness_unto_death.txt"}

    assert sources == expected_sources, f"Expected sources {expected_sources}, found {sources}"

    # Specific keywords we expect
    keywords = ["Abraham", "despair", "paradox", "spirit"]
    found_keywords = {k: False for k in keywords}

    for item in dataset:
        text = item["text"]
        for keyword in keywords:
            if keyword in text:
                found_keywords[keyword] = True

    # Assert all keywords were found across the dataset
    for keyword, found in found_keywords.items():
        assert found, f"Keyword '{keyword}' not found in dataset"

if __name__ == "__main__":
    test_load_kierkegaard_dataset()
