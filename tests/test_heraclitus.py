import pytest
from socials_data.core.loader import load_dataset

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

    # Check source name
    assert first_item["source"] == "fragments.txt"

    # Specific keywords we expect in Heraclitus's text
    keywords = ["logos", "river", "fire", "nature", "harmony"]
    found_keywords = False

    # Since we likely have one big chunk, we check inside it
    for keyword in keywords:
        if keyword in text.lower():
            found_keywords = True
            break

    assert found_keywords, "Did not find expected keywords in the dataset"

if __name__ == "__main__":
    test_load_heraclitus_dataset()
