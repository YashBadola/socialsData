import pytest
from socials_data import load_dataset

def test_load_wittgenstein_dataset():
    """Test that the Wittgenstein dataset can be loaded and contains valid data."""
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
    expected_sources = {"tractatus.txt"}

    # We allow subsets if processing splits it differently, but here we just put one file
    assert sources.issubset(expected_sources), f"Found unexpected sources: {sources - expected_sources}"

    # Specific keywords we expect in Wittgenstein's text
    # Note: "The world is everything that is the case" is the standard Ogden translation for "Die Welt ist alles, was der Fall ist."
    keywords = [
        "The world is everything that is the case",
        "atomic facts",
        "logical space",
        "tautology",
        "Whereof one cannot speak, thereof one must be silent"
    ]

    # Concatenate all text to search
    all_text = " ".join(item["text"] for item in dataset)

    for keyword in keywords:
        assert keyword in all_text, f"Missing keyword: {keyword}"

if __name__ == "__main__":
    test_load_wittgenstein_dataset()
