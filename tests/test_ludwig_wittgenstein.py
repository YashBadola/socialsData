from socials_data import load_dataset
import pytest

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
    expected_source = "tractatus.md"
    assert expected_source in sources, f"Expected source {expected_source} not found in {sources}"

    # Specific keywords we expect in Wittgenstein's text
    keywords = ["world", "logic", "proposition", "silence", "fact"]
    found_keywords = False

    # Concatenate all text to search efficiently
    all_text = " ".join([item["text"] for item in dataset])

    for keyword in keywords:
        if keyword in all_text:
            found_keywords = True
            break

    assert found_keywords, "Did not find expected keywords in the dataset"

    # Check for specific famous quotes (fragments)
    assert "Whereof one cannot speak" in all_text
    assert "The world is everything that is the case" in all_text

if __name__ == "__main__":
    test_load_wittgenstein_dataset()
