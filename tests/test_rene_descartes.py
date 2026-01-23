import pytest
from socials_data.core.loader import load_dataset

def test_load_rene_descartes_dataset():
    """Test that the René Descartes dataset can be loaded and contains valid data."""
    # The directory is named 'rené_descartes'
    dataset = load_dataset("rené_descartes")

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
    expected_source = "discourse_on_method.txt"
    assert expected_source in sources, f"Expected source {expected_source} not found. Found: {sources}"

    # Specific keywords we expect in Descartes' text
    keywords = ["reason", "truth", "God", "soul", "method"]
    found_keywords = False
    for item in dataset:
        for keyword in keywords:
            if keyword in item["text"]:
                found_keywords = True
                break
        if found_keywords:
            break

    assert found_keywords, "Did not find expected keywords in the dataset"

if __name__ == "__main__":
    test_load_rene_descartes_dataset()
