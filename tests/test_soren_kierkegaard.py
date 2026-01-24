import pytest
from socials_data import load_dataset

def test_load_kierkegaard_dataset():
    """Test that the Søren Kierkegaard dataset can be loaded and contains valid data."""
    # Updated ID to 'soren_kierkegaard'
    dataset = load_dataset("soren_kierkegaard")

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
    expected_sources = {"fear_and_trembling.txt", "the_sickness_unto_death.txt"}

    # We expect exactly these two sources
    assert sources == expected_sources, f"Expected sources {expected_sources}, but found {sources}"

    # Specific keywords we expect in Kierkegaard's text
    keywords = ["faith", "anxiety", "self", "infinite", "finite", "paradox"]
    found_keywords = False

    all_text = " ".join([item["text"] for item in dataset]).lower()

    for keyword in keywords:
        if keyword in all_text:
            found_keywords = True
            break

    assert found_keywords, f"Did not find any of the expected keywords: {keywords}"

if __name__ == "__main__":
    test_load_kierkegaard_dataset()
