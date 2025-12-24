import os
import pytest
from socials_data.core.loader import load_dataset
import json

def test_load_rousseau_dataset():
    # Load the dataset
    dataset = load_dataset("jean_jacques_rousseau")

    # Check if dataset is not empty
    assert len(dataset) > 0, "Dataset should not be empty"

    # Check first item structure
    first_item = dataset[0]
    assert "text" in first_item, "Item should have 'text' field"
    assert "source" in first_item, "Item should have 'source' field"

    # Check content of a sample
    found_keyword = False
    keywords = ["nature", "freedom", "liberty", "man", "society", "laws", "will"]

    for i in range(min(100, len(dataset))):
        text = dataset[i]["text"].lower()
        if any(k in text for k in keywords):
            found_keyword = True
            break

    assert found_keyword, "Should find Rousseau-related keywords in the first 100 chunks"

    # Check for absence of Project Gutenberg headers
    for i in range(min(100, len(dataset))):
        text = dataset[i]["text"]
        assert "Project Gutenberg" not in text, "Text should be cleaned of Project Gutenberg headers"
        assert "START OF THE PROJECT" not in text, "Text should be cleaned of start markers"

def test_metadata_exists():
    # Fix the path resolution logic
    # __file__ is tests/test_jean_jacques_rousseau.py
    # os.path.abspath(__file__) is /app/tests/test_jean_jacques_rousseau.py
    # dirname is /app/tests
    # dirname(dirname) is /app

    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    metadata_path = os.path.join(base_dir, "socials_data", "personalities", "jean_jacques_rousseau", "metadata.json")

    assert os.path.exists(metadata_path), f"Metadata file should exist at {metadata_path}"

    with open(metadata_path, 'r') as f:
        data = json.load(f)
        assert data["name"] == "Jean-Jacques Rousseau"
        assert len(data["sources"]) == 3
