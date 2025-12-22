import os
import pytest
from socials_data import load_dataset

def test_load_dataset_plato():
    dataset = load_dataset("plato")
    assert len(dataset) > 0
    # Check that the text contains some expected content
    # Since we have "The Republic" and "Apology", we expect "Socrates" to appear.

    # We can check a few samples
    found_socrates = False
    for item in dataset:
        if "Socrates" in item['text']:
            found_socrates = True
            break

    assert found_socrates, "Dataset should contain mentions of Socrates"

def test_dataset_structure():
    dataset = load_dataset("plato")
    sample = dataset[0]
    assert "text" in sample
    assert isinstance(sample["text"], str)
