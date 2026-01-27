import pytest
from socials_data.core.loader import load_dataset

def test_load_wittgenstein_dataset():
    """Test that the Wittgenstein dataset can be loaded and contains valid data."""
    dataset = load_dataset("ludwig_wittgenstein")

    # Check if dataset is not empty
    assert len(dataset) > 0, "Dataset should not be empty"

    # Check the structure of the first item
    first_item = dataset[0]
    assert "text" in first_item, "Item should contain 'text' field"
    assert "source" in first_item, "Item should contain 'source' field"

    # Check sources
    sources = set(item["source"] for item in dataset)
    expected_sources = {"tractatus.txt", "investigations.txt"}

    assert sources.issubset(expected_sources), f"Found unexpected sources: {sources - expected_sources}"
    assert len(sources) == 2, f"Expected 2 sources, found {len(sources)}"

    # Specific keywords we expect in Wittgenstein's text
    keywords = ["language-games", "family resemblances", "atomic facts", "fly-bottle"]
    found_keywords = 0
    for item in dataset:
        for keyword in keywords:
            if keyword in item["text"]:
                found_keywords += 1

    assert found_keywords > 0, "Did not find expected keywords in the dataset"

if __name__ == "__main__":
    test_load_wittgenstein_dataset()
