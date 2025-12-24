import os
import pytest
from socials_data import load_dataset

def test_aristotle_dataset_loading():
    """Test that the Aristotle dataset loads correctly."""
    dataset = load_dataset("aristotle")
    assert dataset is not None, "Dataset should not be None"
    assert len(dataset) > 0, "Dataset should not be empty"

    # Check structure
    sample = dataset[0]
    assert "text" in sample, "Sample should contain 'text' field"
    assert "source" in sample, "Sample should contain 'source' field"

    # Verify content presence (simple keyword check)
    all_text = " ".join([d["text"] for d in dataset])
    assert "Aristotle" in all_text or "virtue" in all_text or "happiness" in all_text, \
        "Dataset should contain relevant text (Aristotle, virtue, happiness)"

def test_aristotle_files_exist():
    """Test that expected raw files exist."""
    base_dir = os.path.dirname(os.path.abspath(__file__))
    # Adjust path to point to the root of the repo
    repo_root = os.path.abspath(os.path.join(base_dir, ".."))

    raw_dir = os.path.join(repo_root, "socials_data", "personalities", "aristotle", "raw")

    expected_files = ["nicomachean_ethics.txt", "politics.txt", "poetics.txt"]
    for f in expected_files:
        assert os.path.exists(os.path.join(raw_dir, f)), f"Raw file {f} should exist"

def test_aristotle_metadata():
    """Test that metadata is correct."""
    import json
    base_dir = os.path.dirname(os.path.abspath(__file__))
    repo_root = os.path.abspath(os.path.join(base_dir, ".."))
    metadata_path = os.path.join(repo_root, "socials_data", "personalities", "aristotle", "metadata.json")

    with open(metadata_path, 'r') as f:
        metadata = json.load(f)

    assert metadata["name"] == "Aristotle"
    assert metadata["id"] == "aristotle"
    assert len(metadata["sources"]) == 3
