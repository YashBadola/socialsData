import pytest
from socials_data import load_dataset

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
    assert len(sources) == len(expected_sources), f"Missing sources: {expected_sources - sources}"

    # Specific keywords we expect in Heraclitus's text
    keywords = ["Reason", "fire", "river", "strife", "oppositi", "Homer"]
    found_keywords = {k: False for k in keywords}

    for item in dataset:
        for keyword in keywords:
            if keyword in item["text"]:
                found_keywords[keyword] = True

    for keyword, found in found_keywords.items():
        assert found, f"Did not find expected keyword '{keyword}' in the dataset"

if __name__ == "__main__":
    test_load_heraclitus_dataset()
