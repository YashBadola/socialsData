import pytest
from socials_data.core.loader import load_dataset

def test_load_jean_paul_sartre_dataset():
    """Test that the Jean-Paul Sartre dataset can be loaded and contains valid data."""
    dataset = load_dataset("jean_paul_sartre")

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
    expected_sources = {
        "01_intro_reproaches.txt",
        "02_existence_precedes_essence.txt",
        "03_anguish_abandonment.txt",
        "04_despair_and_action.txt",
        "05_subjectivity_and_others.txt",
        "06_existential_humanism.txt",
        "07_conclusion.txt"
    }

    assert sources.issubset(expected_sources), f"Found unexpected sources: {sources - expected_sources}"
    assert len(sources) == len(expected_sources), f"Missing sources: {expected_sources - sources}"

    # Specific keywords we expect in Sartre's text
    keywords = ["existentialism", "freedom", "choice", "anguish", "humanism"]
    found_keywords = False
    for item in dataset:
        for keyword in keywords:
            if keyword in item["text"]:
                found_keywords = True
                break
        if found_keywords:
            break

    assert found_keywords, "Did not find expected keywords in the dataset"
