import os
import pytest
from socials_data import load_dataset

def test_load_dataset_immanuel_kant():
    """Verify that the Immanuel Kant dataset can be loaded."""
    ds = load_dataset("immanuel_kant")

    assert ds is not None
    assert len(ds) > 0

    # Check the first sample
    sample = ds[0]
    assert "text" in sample
    assert isinstance(sample["text"], str)
    assert len(sample["text"]) > 0

    # Check for keywords that should appear in the text
    # Since we loaded "The Critique of Pure Reason", we expect some Kantian terms
    # However, because of chunking, the first chunk might be introductory.
    # Let's check if *any* sample contains specific keywords if the dataset is small enough to iterate quickly,
    # or just check a few samples.

    keywords = ["reason", "pure", "critique", "knowledge", "priori", "experience"]
    found_keyword = False

    for i in range(min(len(ds), 100)):
        text = ds[i]["text"].lower()
        if any(k in text for k in keywords):
            found_keyword = True
            break

    assert found_keyword, "Could not find expected Kantian keywords in the first 100 samples."
