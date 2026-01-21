
import pytest
from socials_data.core.loader import load_dataset
import os

def test_kierkegaard_dataset_loading():
    """Test that the Søren Kierkegaard dataset loads correctly."""
    dataset = load_dataset("søren_kierkegaard")

    # Check that we have data
    assert len(dataset) > 0, "Dataset should not be empty"

    # Check the structure of the first item
    item = dataset[0]
    assert "text" in item
    assert "source" in item

    # Check that we have content from both sources
    sources = set(d["source"] for d in dataset)
    assert "fear_and_trembling.txt" in sources
    assert "either_or.txt" in sources

def test_kierkegaard_text_content():
    """Test specific content in the dataset."""
    dataset = load_dataset("søren_kierkegaard")

    text_content = " ".join([d["text"] for d in dataset])

    # Check for specific phrases from the raw data
    assert "teleological suspension of the ethical" in text_content
    assert "brazen bull" in text_content
    assert "Rotation Method" in text_content
