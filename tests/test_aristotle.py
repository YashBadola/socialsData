from socials_data import load_dataset
import pytest

def test_aristotle_load():
    dataset = load_dataset("aristotle")
    assert len(dataset) > 0
    # Concatenate all texts to search for the snippet
    text_blob = " ".join([item["text"] for item in dataset])
    assert "Every art and every inquiry" in text_blob
    assert "scientific proofs" in text_blob
