import pytest
from socials_data import load_dataset

def test_ludwig_wittgenstein_dataset():
    dataset = load_dataset("ludwig_wittgenstein")
    assert len(dataset) > 0
    first_item = dataset[0]
    assert "text" in first_item
    assert "source" in first_item
    assert "The world is everything that is the case" in first_item["text"]
    assert "Whereof one cannot speak" in first_item["text"]
    assert first_item["source"] == "tractatus_excerpts.txt"
