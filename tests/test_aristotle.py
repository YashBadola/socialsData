import os
import pytest
from socials_data import load_dataset
from socials_data.core.manager import PersonalityManager

def test_aristotle_existence():
    """Test that Aristotle exists in the personality list."""
    manager = PersonalityManager()
    personalities = manager.list_personalities()
    assert "aristotle" in personalities

def test_aristotle_load_dataset():
    """Test loading the Aristotle dataset."""
    ds = load_dataset("aristotle")
    assert len(ds) > 0

    # Check that we have content from each book (heuristic based on text length or content)
    # Since we can't easily check which source a chunk came from in the final dataset
    # (unless the source column is populated correctly), we check for key terms.

    # Check schema
    sample = ds[0]
    assert "text" in sample
    assert "source" in sample

    # Collect all text to search for keywords
    all_text = " ".join([row["text"] for row in ds])

    # Nicomachean Ethics keywords
    assert "virtue" in all_text.lower()
    assert "happiness" in all_text.lower()

    # Politics keywords
    assert "state" in all_text.lower() or "city" in all_text.lower()
    assert "citizen" in all_text.lower()

    # Poetics keywords
    assert "tragedy" in all_text.lower()
    assert "imitation" in all_text.lower() or "mimesis" in all_text.lower()

def test_aristotle_metadata():
    """Test metadata integrity."""
    manager = PersonalityManager()
    metadata = manager.get_metadata("aristotle")

    assert metadata["name"] == "Aristotle"
    assert len(metadata["sources"]) == 3
    assert metadata["sources"][0]["title"] == "The Nicomachean Ethics"
