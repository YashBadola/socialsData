import os
import pytest
from socials_data.core.loader import load_dataset
import json

def test_load_wittgenstein_dataset():
    """Test that the Wittgenstein dataset can be loaded and contains valid data."""
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
    assert expected_sources.issubset(sources), f"Missing expected sources: {expected_sources - sources}"

    # Specific keywords we expect
    keywords = ["proposition", "language-game", "silent", "family resemblances", "picture"]
    found_keywords = False
    for item in dataset:
        for keyword in keywords:
            if keyword in item["text"]:
                found_keywords = True
                break
        if found_keywords:
            break

    assert found_keywords, "Did not find expected keywords in the dataset"

def test_qa_dataset_exists():
    """Test that the Q&A dataset file exists and has content."""
    qa_path = os.path.join("socials_data", "personalities", "ludwig_wittgenstein", "processed", "qa.jsonl")
    assert os.path.exists(qa_path), "qa.jsonl should exist"

    with open(qa_path, 'r') as f:
        lines = f.readlines()

    assert len(lines) > 0, "qa.jsonl should not be empty"

    first_qa = json.loads(lines[0])
    assert "instruction" in first_qa
    assert "response" in first_qa
