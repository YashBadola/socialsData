import os
import pytest
from socials_data import load_dataset

def test_soren_kierkegaard_dataset_loading():
    """Test that the Søren Kierkegaard dataset loads correctly."""
    dataset = load_dataset("soren_kierkegaard")

    # Check that it returns a Hugging Face Dataset
    assert str(type(dataset)) == "<class 'datasets.arrow_dataset.Dataset'>"

    # Check that it has data
    assert len(dataset) > 0

    # Check structure
    sample = dataset[0]
    assert "text" in sample
    assert "source" in sample
    assert isinstance(sample["text"], str)
    assert isinstance(sample["source"], str)

    # Check content relevance (look for keywords)
    # Since we have "What is a poet?" right at the beginning, we can check for that or "anguish"
    # or "existential" or "faith".
    # Let's check a few samples until we find a match, to be robust against chunking.

    keywords = ["poet", "anguish", "God", "faith", "music", "soul", "Kierkegaard", "aesthetic", "ethical"]
    found_keyword = False

    for i in range(min(10, len(dataset))):
        text = dataset[i]["text"]
        if any(keyword in text for keyword in keywords):
            found_keyword = True
            break

    assert found_keyword, "Could not find any expected keywords in the first 10 samples."

if __name__ == "__main__":
    test_soren_kierkegaard_dataset_loading()
