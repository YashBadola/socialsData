import os
import pytest
from socials_data.core.loader import load_dataset

def test_load_simone_de_beauvoir_dataset():
    """Test that the Simone de Beauvoir dataset can be loaded and contains valid data."""
    dataset = load_dataset("simone_de_beauvoir")

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
    expected_sources = {"the_second_sex_intro.txt", "ethics_of_ambiguity.txt", "memoirs.txt"}

    # We might not have all chunks from all files in a small sample if we sliced,
    # but the full dataset should have them.
    # Let's just check that the sources present are valid.
    assert sources.issubset(expected_sources), f"Found unexpected sources: {sources - expected_sources}"

    # Specific keywords we expect in Simone de Beauvoir's text
    keywords = ["woman", "freedom", "ambiguity", "existence", "Other"]
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
    test_load_simone_de_beauvoir_dataset()
