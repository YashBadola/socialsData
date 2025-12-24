import pytest
import os
from socials_data import load_dataset

def test_load_machiavelli_dataset():
    # Load the dataset
    dataset = load_dataset("niccolo_machiavelli")

    # Check if dataset is not empty
    assert len(dataset) > 0

    # Check the first item
    first_item = dataset[0]
    assert "text" in first_item
    assert "source" in first_item

    # Check if the content is from The Prince or Discourses
    sources = set(item["source"] for item in dataset)
    assert "the_prince.txt" in sources
    assert "discourses_on_livy.txt" in sources

    # Check for specific keywords
    text_content = " ".join([item["text"] for item in dataset])
    assert "prince" in text_content.lower()
    assert "republic" in text_content.lower()
    assert "virtue" in text_content.lower() or "virtù" in text_content.lower()
