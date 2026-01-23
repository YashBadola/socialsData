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
    expected_source = "fragments.txt"
    assert expected_source in sources, f"Expected source {expected_source} not found"

    # Specific keywords we expect in Heraclitus's text
    keywords = ["Logos", "river", "Fire", "opposites", "war"]
    found_keywords = False

    # Concatenate all text to search for keywords
    all_text = " ".join([item["text"] for item in dataset])

    for keyword in keywords:
        if keyword in all_text:
            found_keywords = True
            break

    assert found_keywords, "Did not find expected keywords in the dataset"

    # Specific fragment check
    assert "same river" in all_text
    assert "Character is destiny" in all_text

if __name__ == "__main__":
    test_load_heraclitus_dataset()
