import pytest
from socials_data.core.loader import load_dataset

def test_load_jean_paul_sartre_dataset():
    """Test that the Jean-Paul Sartre dataset can be loaded and contains valid data."""
    dataset = load_dataset("jean_paul_sartre")

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
    expected_sources = {"existentialism.txt", "bad_faith.txt", "freedom.txt"}

    # Check that expected sources are present in the loaded dataset
    assert sources.issubset(expected_sources), f"Found unexpected sources: {sources - expected_sources}"
    assert expected_sources.issubset(sources), f"Missing expected sources: {expected_sources - sources}"

    # Specific keywords we expect in Sartre's text
    keywords = ["existence precedes essence", "bad faith", "condemned to be free", "waiter"]
    found_keywords = {keyword: False for keyword in keywords}

    for item in dataset:
        for keyword in keywords:
            if keyword in item["text"]:
                found_keywords[keyword] = True

    # Check that all keywords were found across the dataset
    missing_keywords = [k for k, found in found_keywords.items() if not found]
    assert not missing_keywords, f"Did not find expected keywords: {missing_keywords}"

if __name__ == "__main__":
    test_load_jean_paul_sartre_dataset()
