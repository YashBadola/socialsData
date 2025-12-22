import os
import pytest
from socials_data import load_dataset

def test_load_dataset_immanuel_kant():
    """Verify that the Immanuel Kant dataset loads correctly."""
    dataset = load_dataset("immanuel_kant")

    assert len(dataset) > 0, "Dataset should not be empty"

    # Check the first few samples
    samples = dataset[:5]
    assert "text" in samples, "Dataset should have a 'text' column"
    assert "source" in samples, "Dataset should have a 'source' column"

    # Check content of a sample
    first_text = samples["text"][0]
    assert isinstance(first_text, str), "Text should be a string"
    assert len(first_text) > 0, "Text should not be empty"

    # Check that we have data from all sources
    # Note: dataset["source"] in a slice gives a list of sources for those items.
    # To check all sources, we should iterate over the dataset or check unique values
    # if the dataset is small enough, or just pick random samples.

    unique_sources = set(dataset["source"])
    print(f"Found sources: {unique_sources}")

    expected_sources = {
        "critique_of_pure_reason.txt",
        "critique_of_practical_reason.txt",
        "metaphysic_of_morals.txt"
    }

    # Check if we have at least one of the expected sources
    assert len(unique_sources.intersection(expected_sources)) > 0, f"Expected one of {expected_sources}, but found {unique_sources}"

    print("Immanuel Kant dataset verification passed.")

if __name__ == "__main__":
    test_load_dataset_immanuel_kant()
