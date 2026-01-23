import pytest
from socials_data.core.loader import load_dataset

def test_load_ludwig_wittgenstein_dataset():
    """Test that the Ludwig Wittgenstein dataset can be loaded and contains valid data."""
    dataset = load_dataset("ludwig_wittgenstein")

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
    expected_sources = {"tractatus.txt", "philosophical_investigations.txt"}

    # Check that sources present are valid
    assert sources.issubset(expected_sources), f"Found unexpected sources: {sources - expected_sources}"

    # Specific keywords we expect in Wittgenstein's text
    keywords = ["world", "facts", "silent", "language-games", "meaning"]
    found_keywords = False

    # Iterate through all items to find keywords
    all_text = " ".join([item["text"] for item in dataset])

    for keyword in keywords:
        if keyword in all_text:
            found_keywords = True
        else:
            # We want to ensure all keywords are found across the dataset for this specific curated set
            # But the original test logic was "if any keyword found", let's be stricter here since we know the content.
            pass

    # Re-evaluating the keyword check logic based on the original test_plato.py
    # Plato test checks if AT LEAST ONE keyword is found.
    # "assert found_keywords" means at least one.

    # But since I curated the text, I expect ALL of them to be there.
    for keyword in keywords:
         assert keyword in all_text, f"Keyword '{keyword}' not found in dataset"

if __name__ == "__main__":
    test_load_ludwig_wittgenstein_dataset()
