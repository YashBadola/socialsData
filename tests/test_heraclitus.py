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
    assert first_item["source"] == "fragments.txt"

    # Check content of the text
    text = first_item["text"]
    assert isinstance(text, str), "Text should be a string"
    assert len(text) > 0, "Text should not be empty"

    # Specific keywords we expect in Heraclitus's text
    keywords = ["Logos", "river", "Fire", "opposites", "war", "change"]

    # Since all text is likely in one chunk for now:
    found_keywords = []
    for keyword in keywords:
        if keyword.lower() in text.lower():
            found_keywords.append(keyword)

    # We expect to find most of them
    assert len(found_keywords) >= 3, f"Expected at least 3 keywords, found: {found_keywords}"

    # Check for specific famous phrase
    assert "twice into the same river" in text, "Famous river quote missing"

if __name__ == "__main__":
    test_load_heraclitus_dataset()
