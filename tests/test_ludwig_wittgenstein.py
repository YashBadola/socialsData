import os
import json
import pytest
from socials_data.core.loader import load_dataset

def test_load_ludwig_wittgenstein_dataset():
    """Test that the Ludwig Wittgenstein dataset can be loaded and contains valid data."""
    dataset = load_dataset("ludwig_wittgenstein")

    # Check if dataset is not empty
    assert len(dataset) > 0, "Dataset should not be empty"

    # Check the structure of the first item
    first_item = dataset[0]
    assert "text" in first_item, "Item should contain 'text' field"
    assert "source" in first_item, "Item should contain 'source' field"

    # Check content of the text
    text = first_item["text"]
    assert isinstance(text, str), "Text should be a string"
    assert len(text) > 0, "Text should not be empty"

    # Check sources
    sources = set(item["source"] for item in dataset)
    expected_sources = {"tractatus.txt", "philosophical_investigations.txt"}
    assert sources.issubset(expected_sources), f"Found unexpected sources: {sources - expected_sources}"

    # Specific keywords we expect
    keywords = ["proposition", "silent", "language-game", "meaning"]
    found_keywords = {k: False for k in keywords}

    for item in dataset:
        for keyword in keywords:
            if keyword in item["text"]:
                found_keywords[keyword] = True

    for keyword, found in found_keywords.items():
        assert found, f"Did not find expected keyword '{keyword}' in the dataset"

def test_verify_qa_data():
    """Test that QA data exists and has correct structure."""
    qa_path = "socials_data/personalities/ludwig_wittgenstein/processed/qa.jsonl"
    assert os.path.exists(qa_path), "qa.jsonl should exist"

    with open(qa_path, "r", encoding="utf-8") as f:
        lines = f.readlines()
        assert len(lines) > 0, "qa.jsonl should not be empty"

        for line in lines:
            data = json.loads(line)
            assert "instruction" in data, "QA item should have 'instruction'"
            assert "response" in data, "QA item should have 'response'"
            assert "source" in data, "QA item should have 'source'"

if __name__ == "__main__":
    test_load_ludwig_wittgenstein_dataset()
    test_verify_qa_data()
