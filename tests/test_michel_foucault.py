import pytest
from socials_data.core.loader import load_dataset

def test_load_michel_foucault_dataset():
    """Test that the Michel Foucault dataset can be loaded and contains valid data."""
    dataset = load_dataset("michel_foucault")

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
    expected_sources = {"panopticism.txt", "history_of_sexuality.txt", "madness_and_civilization.txt"}

    assert sources.issubset(expected_sources), f"Found unexpected sources: {sources - expected_sources}"
    assert len(sources) == 3, f"Expected 3 sources, found {len(sources)}"

    # Specific keywords we expect in Foucault's text
    keywords = ["Panopticon", "power", "sexuality", "madness", "confinement"]
    found_keywords = set()
    for item in dataset:
        for keyword in keywords:
            if keyword in item["text"]:
                found_keywords.add(keyword)

    assert len(found_keywords) > 0, "Did not find expected keywords in the dataset"

if __name__ == "__main__":
    test_load_michel_foucault_dataset()
