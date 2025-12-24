import os
import pytest
from socials_data.core.loader import load_dataset

def test_aristotle_dataset_exists():
    """Test that the Aristotle dataset can be loaded."""
    # Ensure proper path setup as per memory
    dataset = load_dataset("aristotle")
    assert dataset is not None
    assert len(dataset) > 0

def test_aristotle_content():
    """Test that the content contains expected Aristotle text."""
    dataset = load_dataset("aristotle")

    # Check for keywords from his works
    keywords = ["virtue", "happiness", "political", "tragedy", "imitation"]
    found_keywords = {k: False for k in keywords}

    # We check a sample of entries to find keywords
    # Since dataset is not split-aware, we iterate directly
    # Using a subset to be faster if the dataset is huge
    sample_size = min(len(dataset), 1000)

    for i in range(sample_size):
        text = dataset[i]['text'].lower()
        for k in keywords:
            if k in text:
                found_keywords[k] = True

    # Assert we found at least some keywords (not necessarily all in the first 1000 chunks, but likely)
    # "virtue" and "happiness" are very common in Ethics. "political" in Politics. "tragedy" in Poetics.

    # We expect at least one keyword to be found to verify it's not empty or garbage
    assert any(found_keywords.values()), f"No keywords found in sample: {found_keywords}"

    # Let's try to find specific ones to be sure
    if len(dataset) > 50:
        assert found_keywords["virtue"] or found_keywords["happiness"] or found_keywords["political"], "Core Aristotle concepts not found"

def test_aristotle_metadata_structure():
    """Test the directory structure and metadata."""
    base_path = os.path.dirname(os.path.abspath(__file__))
    # Adjust path to reach the package root if needed, but here we construct relative to this test file
    # tests/ is at root, socials_data/ is at root
    # So ../socials_data

    repo_root = os.path.dirname(base_path)
    aristotle_path = os.path.join(repo_root, "socials_data", "personalities", "aristotle")

    assert os.path.exists(aristotle_path)
    assert os.path.exists(os.path.join(aristotle_path, "metadata.json"))
    assert os.path.exists(os.path.join(aristotle_path, "processed", "data.jsonl"))
    # qa.jsonl might not exist since we skipped it
