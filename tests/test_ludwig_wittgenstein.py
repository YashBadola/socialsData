import os
import pytest
from socials_data.core.loader import load_dataset
import json

def test_load_wittgenstein_dataset():
    """Test that the Ludwig Wittgenstein dataset can be loaded and contains valid data."""
    dataset = load_dataset("ludwig_wittgenstein")

    # Check if dataset is not empty
    assert len(dataset) > 0, "Dataset should not be empty"

    # Check structure
    first_item = dataset[0]
    assert "text" in first_item, "Item should contain 'text' field"
    assert "source" in first_item, "Item should contain 'source' field"

    # Check sources
    sources = set(item["source"] for item in dataset)
    expected_sources = {"tractatus.txt", "philosophical_investigations.txt", "culture_and_value.txt"}
    assert sources.issubset(expected_sources), f"Found unexpected sources: {sources - expected_sources}"
    assert sources == expected_sources, f"Missing sources: {expected_sources - sources}"

    # Check content keywords
    keywords = ["language-game", "beetle", "silent", "atomic facts", "music"]
    found_keywords = {k: False for k in keywords}

    for item in dataset:
        text = item["text"].lower()
        for k in keywords:
            if k in text:
                found_keywords[k] = True

    assert all(found_keywords.values()), f"Missing keywords in text: {[k for k, v in found_keywords.items() if not v]}"

def test_qa_file_exists():
    """Test that the QA file exists and is valid JSONL."""
    qa_path = os.path.join("socials_data", "personalities", "ludwig_wittgenstein", "processed", "qa.jsonl")
    assert os.path.exists(qa_path), "QA file does not exist"

    with open(qa_path, "r") as f:
        for line in f:
            item = json.loads(line)
            assert "instruction" in item
            assert "response" in item
            assert "source" in item

if __name__ == "__main__":
    test_load_wittgenstein_dataset()
    test_qa_file_exists()
