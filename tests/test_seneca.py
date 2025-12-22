import pytest
from socials_data import load_dataset
from datasets import Dataset

def test_load_seneca_dataset():
    """Test loading the Seneca dataset."""
    dataset = load_dataset("seneca")
    assert isinstance(dataset, Dataset)
    assert len(dataset) > 0

    # Check first sample
    sample = dataset[0]
    assert "text" in sample
    assert isinstance(sample["text"], str)
    assert len(sample["text"]) > 0

    # Check for keywords that should appear in Seneca's text
    # Since we have "Morals of a Happy Life" and "On Benefits", words like "virtue", "benefit", "nature" should be common.
    # We'll scan a few samples to find one.
    found_keyword = False
    keywords = ["virtue", "benefit", "nature", "happy", "anger", "clemency", "Stoic", "Seneca", "Lucilius"]

    for item in dataset:
        text = item["text"].lower()
        if any(k.lower() in text for k in keywords):
            found_keyword = True
            break

    assert found_keyword, "Did not find expected keywords in the dataset."
