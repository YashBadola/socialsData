import pytest
from socials_data import load_dataset

def test_load_kierkegaard_dataset():
    dataset = load_dataset("soren_kierkegaard")
    assert len(dataset) > 0
    assert "text" in dataset[0]
    assert "source" in dataset[0]
    assert dataset[0]["source"] == "selections.txt"
