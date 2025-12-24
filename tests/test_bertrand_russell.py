import os
import pytest
from socials_data import load_dataset

PERSONALITY_ID = "bertrand_russell"

def test_load_dataset():
    # Load the dataset
    dataset = load_dataset(PERSONALITY_ID)

    # Check if dataset is not empty
    assert len(dataset) > 0, "Dataset should not be empty"

    # Check structure
    assert "text" in dataset.column_names, "Dataset should contain 'text' column"
    assert "source" in dataset.column_names, "Dataset should contain 'source' column"

    # Check content of a sample
    sample = dataset[0]
    assert isinstance(sample["text"], str), "Text should be a string"
    assert len(sample["text"]) > 100, "Text should be reasonably long"

    # Check for specific keywords related to Russell
    text_content = "".join([d["text"] for d in dataset])
    assert "philosophy" in text_content.lower(), "Should contain 'philosophy'"
    assert "logic" in text_content.lower(), "Should contain 'logic'"

    # Check that Gutenberg license is removed (basic check)
    assert "Project Gutenberg License" not in text_content, "License text should be removed"

def test_sources_present():
    dataset = load_dataset(PERSONALITY_ID)
    sources = set(dataset["source"])

    expected_sources = {
        "the_problems_of_philosophy.txt",
        "the_analysis_of_mind.txt",
        "mysticism_and_logic.txt"
    }

    # Check if all expected sources are present
    # Note: Depending on how `process` works, it might split files or keep them whole.
    # If it keeps them whole, we expect exactly these sources.
    # If it splits, we expect these filenames to appear in the source column.

    for expected in expected_sources:
        assert expected in sources, f"Source {expected} should be present in the dataset"

if __name__ == "__main__":
    test_load_dataset()
    test_sources_present()
    print("Tests passed!")
