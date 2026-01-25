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

    # Specific keywords we expect in Heraclitus's text
    keywords = ["Logos", "river", "fire", "change", "flux", "war", "harmony"]
    found_keywords = False

    # We only have one chunk in the current setup, but iterating is safer if that changes
    for item in dataset:
        for keyword in keywords:
            if keyword in item["text"]: # Case sensitive matching as per original text
                found_keywords = True
                break
            if keyword.lower() in item["text"].lower():
                 found_keywords = True
                 break
        if found_keywords:
            break

    assert found_keywords, "Did not find expected keywords in the dataset"

    # Verify specific famous fragments
    all_text = " ".join([item["text"] for item in dataset])
    assert "step twice into the same river" in all_text
    assert "Character is destiny" in all_text

if __name__ == "__main__":
    test_load_heraclitus_dataset()
