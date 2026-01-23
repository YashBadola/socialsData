import os
import pytest
from socials_data.core.loader import load_dataset
import json

def test_load_wittgenstein_dataset():
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

    # We might not have all chunks from all files in a small sample if we sliced,
    # but the full dataset should have them.
    assert sources.issubset(expected_sources), f"Found unexpected sources: {sources - expected_sources}"

    # Specific keywords we expect in Wittgenstein's text
    keywords = ["world", "logic", "language", "game", "fly-bottle", "silent"]
    found_keywords = False
    for item in dataset:
        for keyword in keywords:
            if keyword in item["text"]:
                found_keywords = True
                break
        if found_keywords:
            break

    assert found_keywords, "Did not find expected keywords in the dataset"

def test_wittgenstein_qa_dataset():
    """Test that the QA dataset exists and is valid."""
    # Assuming we can load it manually or via future API.
    # For now, let's check the file directly as the loader primarily handles 'data.jsonl'
    # (Though the README mentions 'load_dataset defaults to text', implying we can load others)

    # We will just verify the file content directly for this test
    qa_path = "socials_data/personalities/ludwig_wittgenstein/processed/qa.jsonl"
    assert os.path.exists(qa_path), "QA file should exist"

    with open(qa_path, "r") as f:
        lines = f.readlines()
        assert len(lines) > 0, "QA file should not be empty"

        for line in lines:
            data = json.loads(line)
            assert "instruction" in data
            assert "response" in data
            assert "source" in data

if __name__ == "__main__":
    test_load_wittgenstein_dataset()
    test_wittgenstein_qa_dataset()
