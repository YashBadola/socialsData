import pytest
from socials_data import load_dataset
from datasets import Dataset

def test_load_dataset_kant():
    """Test that the Immanuel Kant dataset loads correctly and contains data."""
    dataset = load_dataset("immanuel_kant")

    # Check that it returns a Dataset object
    assert isinstance(dataset, Dataset)

    # Check that it is not empty
    assert len(dataset) > 0

    # Check first sample structure
    sample = dataset[0]
    assert "text" in sample
    assert isinstance(sample["text"], str)
    assert len(sample["text"]) > 0
    assert "source" in sample

    # Check content relevance (look for keywords)
    # Since we are sampling, we might not get these specific words in the first chunk,
    # but let's check if *any* chunk has "reason" or "moral" or "transcendental"

    found_keyword = False
    keywords = ["reason", "moral", "transcendental", "imperative", "law", "duty"]

    # Check a few samples
    for i in range(min(len(dataset), 20)):
        text = dataset[i]["text"].lower()
        if any(k in text for k in keywords):
            found_keyword = True
            break

    assert found_keyword, "Did not find expected Kantian keywords in the first few samples."
