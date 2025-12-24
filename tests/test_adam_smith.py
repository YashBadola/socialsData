import pytest
import os
from pathlib import Path
from socials_data import load_dataset
import json

@pytest.fixture
def dataset():
    # Force reload or clean env if necessary, but load_dataset should work
    return load_dataset("adam_smith")

def test_adam_smith_dataset_structure(dataset):
    """Test that the Adam Smith dataset has the correct structure."""
    assert len(dataset) > 0
    assert "text" in dataset.column_names
    assert "source" in dataset.column_names

def test_adam_smith_content(dataset):
    """Test that the content is relevant to Adam Smith."""
    # Check for keywords
    keywords = ["labour", "market", "wealth", "moral", "sentiment", "sympathy"]

    found_keywords = {kw: False for kw in keywords}

    # Check a sample of the data
    for item in dataset:
        text = item["text"].lower()
        for kw in keywords:
            if kw in text:
                found_keywords[kw] = True

    # We expect to find most of these keywords
    assert found_keywords["labour"], "Keyword 'labour' not found"
    assert found_keywords["wealth"], "Keyword 'wealth' not found"

    # 'sympathy' might be in Moral Sentiments
    assert found_keywords["sympathy"], "Keyword 'sympathy' not found"

def test_adam_smith_sources(dataset):
    """Test that the sources are correct."""
    sources = set(dataset["source"])
    expected_sources = {"wealth_of_nations.txt", "moral_sentiments.txt", "essays.txt"}
    assert sources == expected_sources

def test_no_gutenberg_artifacts(dataset):
    """Test that Project Gutenberg headers/footers are removed."""
    for item in dataset:
        text = item["text"]
        assert "START OF THE PROJECT GUTENBERG" not in text
        assert "END OF THE PROJECT GUTENBERG" not in text
        # Also check for license text usually at the end
        assert "subscribe to our email newsletter" not in text
