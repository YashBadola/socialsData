import pytest
from socials_data import load_dataset

def test_load_kierkegaard_dataset():
    """Test that the Søren Kierkegaard dataset can be loaded and contains valid data."""
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
    expected_source_part = "works.txt"

    # Since we have one file 'works.txt', we expect it to be present.
    assert any(expected_source_part in s for s in sources), f"Expected source {expected_source_part} not found in {sources}"

    # Specific keywords we expect in Kierkegaard's text
    keywords = ["Abraham", "Isaac", "despair", "spirit", "self"]
    found_keywords = False

    # Concatenate all text to search for keywords
    all_text = " ".join([item["text"] for item in dataset])

    for keyword in keywords:
        if keyword in all_text:
            found_keywords = True
            break # Found at least one

    assert found_keywords, f"Did not find any of the expected keywords {keywords} in the dataset"

    # Specific check for a famous line
    assert "infinite and the finite" in all_text, "Expected 'infinite and the finite' phrase not found"

if __name__ == "__main__":
    test_load_kierkegaard_dataset()
