import os
import pytest
from socials_data import load_dataset

def test_load_dataset_immanuel_kant():
    """Test loading the Immanuel Kant dataset."""
    dataset = load_dataset("immanuel_kant")

    assert dataset is not None, "Dataset should not be None"
    assert len(dataset) > 0, "Dataset should contain entries"

    # Check schema
    sample = dataset[0]
    assert "text" in sample, "Sample should contain 'text' field"
    assert "source" in sample, "Sample should contain 'source' field"

    # Check content relevance (basic check)
    # Search for a keyword likely to be in the first few chunks or at least one chunk
    found_keyword = False
    keywords = ["reason", "critique", "moral", "law", "experience", "phenomena", "noumena", "imperative"]

    # Check a few samples
    for i in range(min(100, len(dataset))):
        text = dataset[i]["text"].lower()
        if any(k in text for k in keywords):
            found_keyword = True
            break

    assert found_keyword, f"Dataset text should contain relevant keywords: {keywords}"

def test_files_exist():
    """Test that the processed files exist."""
    base_path = "socials_data/personalities/immanuel_kant"
    assert os.path.exists(os.path.join(base_path, "processed", "data.jsonl")), "processed/data.jsonl should exist"
    assert os.path.exists(os.path.join(base_path, "metadata.json")), "metadata.json should exist"
