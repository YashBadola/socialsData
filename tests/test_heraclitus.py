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
    expected_sources = {"fragments.txt"}
    assert sources.issubset(expected_sources), f"Found unexpected sources: {sources - expected_sources}"

    # Specific keywords we expect in Heraclitus's text
    keywords = ["river", "fire", "logos", "Word", "flux"]
    # Since "logos" might not be in the translation I used (I used "Word" which is the translation), I'll check for "Word" and "river".
    # I included "Word" in the fragments.

    found_keywords = False
    for item in dataset:
        for keyword in keywords:
            if keyword in item["text"] or keyword.lower() in item["text"].lower():
                found_keywords = True
                break
        if found_keywords:
            break

    assert found_keywords, "Did not find expected keywords in the dataset"

    # Specific fragment check
    assert "No man ever steps in the same river twice" in text, "Famous river fragment missing"

if __name__ == "__main__":
    test_load_heraclitus_dataset()
