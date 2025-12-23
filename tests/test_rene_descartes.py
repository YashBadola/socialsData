import pytest
import os
from socials_data import load_dataset

def test_load_rene_descartes_dataset():
    """Test loading the Rene Descartes dataset."""
    dataset = load_dataset("rene_descartes")

    assert dataset is not None
    assert len(dataset) > 0

    # Check a sample
    sample = dataset[0]
    assert "text" in sample
    assert isinstance(sample["text"], str)
    assert len(sample["text"]) > 0
    assert "source" in sample

    # Check for content keywords
    # We need to iterate to find specific keywords because the dataset is chunked
    found_method = False
    found_meditation = False
    found_principles = False

    for item in dataset:
        text = item["text"].lower()
        if "discourse" in text or "method" in text:
            found_method = True
        if "meditation" in text or "god" in text:
            found_meditation = True
        if "principle" in text or "philosophy" in text:
            found_principles = True

        if found_method and found_meditation and found_principles:
            break

    assert found_method, "Content from Discourse on Method not found"
    assert found_meditation, "Content from Meditations not found"
    assert found_principles, "Content from Principles not found"

if __name__ == "__main__":
    test_load_rene_descartes_dataset()
    print("Test passed!")
