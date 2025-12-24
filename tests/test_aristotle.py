import pytest
import os
from socials_data import load_dataset

def test_load_dataset_aristotle():
    """Test loading the Aristotle dataset."""
    dataset = load_dataset("aristotle")
    assert len(dataset) > 0

    # Check a sample
    sample = dataset[0]
    assert "text" in sample
    assert "source" in sample
    assert isinstance(sample["text"], str)
    assert len(sample["text"]) > 0

    # Verify content keywords to ensure we have the right texts
    all_text = " ".join([d["text"] for d in dataset])

    # Keywords for Ethics
    assert "virtue" in all_text.lower()
    assert "happiness" in all_text.lower()

    # Keywords for Politics
    assert "state" in all_text.lower() or "city" in all_text.lower()
    assert "constitution" in all_text.lower()

    # Keywords for Poetics
    assert "tragedy" in all_text.lower()
    assert "imitation" in all_text.lower()

    # Keywords for Categories
    assert "substance" in all_text.lower()
    assert "predicate" in all_text.lower()

    # Check for absence of Project Gutenberg headers
    # We check the first few characters of samples or search the whole text for the license preamble
    assert "Project Gutenberg License" not in all_text
    assert "This ebook is for the use of anyone anywhere" not in all_text
    assert "*** START OF THE PROJECT GUTENBERG EBOOK" not in all_text

def test_aristotle_metadata_structure():
    """Verify the metadata file exists and has correct structure."""
    metadata_path = os.path.join(
        os.path.dirname(os.path.abspath(__file__)),
        "../socials_data/personalities/aristotle/metadata.json"
    )
    import json
    with open(metadata_path, 'r') as f:
        metadata = json.load(f)

    assert metadata["name"] == "Aristotle"
    assert metadata["id"] == "aristotle"
    assert len(metadata["sources"]) == 4
