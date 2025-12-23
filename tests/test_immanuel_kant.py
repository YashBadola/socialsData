import os
import pytest
from socials_data import load_dataset

def test_load_dataset_immanuel_kant():
    """Test loading the Immanuel Kant dataset."""
    dataset = load_dataset("immanuel_kant")

    assert dataset is not None
    assert len(dataset) > 0

    # Check the first few samples
    for i in range(min(5, len(dataset))):
        sample = dataset[i]
        assert "text" in sample
        assert "source" in sample
        assert isinstance(sample["text"], str)
        assert len(sample["text"]) > 0

    # Check for content specific to Kant
    # We look for keywords in the whole dataset (or at least one chunk)
    found_keyword = False
    keywords = ["reason", "critique", "metaphysic", "moral", "priori"]

    # Check a subset to avoid slow tests if dataset is huge
    for i in range(min(100, len(dataset))):
        text = dataset[i]["text"].lower()
        if any(k in text for k in keywords):
            found_keyword = True
            break

    assert found_keyword, "Did not find expected keywords in the first 100 samples."

if __name__ == "__main__":
    test_load_dataset_immanuel_kant()
    print("Test passed!")
