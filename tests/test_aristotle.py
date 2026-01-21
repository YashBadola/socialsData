from socials_data.core.loader import load_dataset
import pytest

def test_load_aristotle_dataset():
    dataset = load_dataset("aristotle")
    assert len(dataset) > 0
    assert "text" in dataset[0]
    assert "Aristotle" in dataset[0]["text"]
