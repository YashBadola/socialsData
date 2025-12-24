import os
import pytest
from socials_data import load_dataset

@pytest.fixture
def dataset():
    return load_dataset("jean_jacques_rousseau")

def test_dataset_structure(dataset):
    assert len(dataset) > 0
    sample = dataset[0]
    assert "text" in sample
    assert "source" in sample
    assert isinstance(sample["text"], str)
    assert isinstance(sample["source"], str)

def test_dataset_content(dataset):
    # Check for characteristic phrases
    text = " ".join([d["text"] for d in dataset])

    # Common Rousseau themes
    assert "social contract" in text.lower() or "general will" in text.lower()
    assert "nature" in text.lower()

    # Check that Gutenberg headers are stripped
    assert "*** START OF THE PROJECT GUTENBERG" not in text
    assert "*** END OF THE PROJECT GUTENBERG" not in text

    # Check specific sources are present
    sources = set(d["source"] for d in dataset)
    assert "social_contract.txt" in sources
    assert "confessions.txt" in sources
    assert "emile.txt" in sources
    assert "inequality.txt" in sources

def test_cleanliness(dataset):
    # Ensure no license text remains
    for item in dataset:
        text = item["text"]
        assert "Project Gutenberg License" not in text
        assert "The Project Gutenberg Literary Archive Foundation" not in text
