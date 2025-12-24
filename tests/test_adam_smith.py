import os
import pytest
from socials_data.core.loader import load_dataset
import json

def test_adam_smith_dataset():
    # Load the dataset
    dataset = load_dataset("adam_smith")

    # Check if it returns a Dataset object (not split)
    assert dataset is not None
    # Depending on how load_dataset works, it might return a Dataset or DatasetDict
    # The memory says: "The load_dataset function returns a Hugging Face Dataset object, which is not split-aware"

    # Check if we have data
    assert len(dataset) > 0

    # Check sample structure
    sample = dataset[0]
    assert "text" in sample
    assert "source" in sample

    # Check content relevance
    # Combine some text to check for keywords
    combined_text = " ".join(dataset[:100]["text"]).lower()

    keywords = ["wealth", "labour", "market", "moral", "sentiment", "sympathy", "invisible hand", "propriety"]
    found_keywords = [k for k in keywords if k in combined_text]

    # We expect at least some of these keywords
    assert len(found_keywords) > 0, f"No expected keywords found in the first 100 samples. Found: {found_keywords}"

    # Check sources
    sources = set(dataset["source"])
    expected_sources = {"wealth_of_nations.txt", "theory_of_moral_sentiments.txt"}
    assert sources.intersection(expected_sources) == expected_sources, f"Missing sources. Found: {sources}"

    # Negative assertions (no Gutenberg headers)
    for i in range(min(50, len(dataset))):
        text = dataset[i]["text"]
        assert "Project Gutenberg" not in text
        assert "START OF THE PROJECT" not in text

if __name__ == "__main__":
    test_adam_smith_dataset()
