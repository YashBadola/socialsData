import os
import pytest
from socials_data import load_dataset

def test_load_dataset_seneca():
    dataset = load_dataset("lucius_annaeus_seneca")
    assert len(dataset) > 0
    # Check a few samples
    for i in range(min(5, len(dataset))):
        sample = dataset[i]
        assert "text" in sample
        assert isinstance(sample["text"], str)
        assert len(sample["text"]) > 0

    # Ensure some key terms are present in the dataset (simple check)
    text_combined = " ".join([d["text"] for d in dataset])
    assert "Seneca" in text_combined or "SENECA" in text_combined
    assert "virtue" in text_combined.lower() or "happy" in text_combined.lower()
