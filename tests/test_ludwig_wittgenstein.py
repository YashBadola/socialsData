import pytest
from socials_data import load_dataset

def test_load_wittgenstein_dataset():
    """Test that the Wittgenstein dataset can be loaded and contains valid data."""
    dataset = load_dataset("ludwig_wittgenstein")

    # Check if dataset is not empty
    assert len(dataset) > 0, "Dataset should not be empty"

    # Check sources
    sources = set(item["source"] for item in dataset)
    expected_sources = {"tractatus.txt", "investigations.txt"}

    assert sources.issubset(expected_sources), f"Found unexpected sources: {sources - expected_sources}"
    assert expected_sources.issubset(sources), f"Missing expected sources: {expected_sources - sources}"

    # Specific keywords we expect
    keywords = ["world", "facts", "language-games", "fly-bottle"]
    found_keywords = {k: False for k in keywords}

    for item in dataset:
        text = item["text"]
        for keyword in keywords:
            if keyword in text:
                found_keywords[keyword] = True

    for keyword, found in found_keywords.items():
        assert found, f"Did not find expected keyword '{keyword}' in the dataset"

if __name__ == "__main__":
    test_load_wittgenstein_dataset()
