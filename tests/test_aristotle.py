import os
import pytest
from socials_data.core.loader import load_dataset
from socials_data.core.manager import PersonalityManager

def test_aristotle_exists():
    manager = PersonalityManager()
    personalities = manager.list_personalities()
    assert "aristotle" in personalities

def test_aristotle_metadata():
    manager = PersonalityManager()
    metadata = manager.get_metadata("aristotle")
    assert metadata["name"] == "Aristotle"
    assert "Nicomachean Ethics" in str(metadata["sources"])
    assert "Politics" in str(metadata["sources"])
    assert "Poetics" in str(metadata["sources"])
    assert "empiricist" in metadata["system_prompt"]

def test_load_dataset():
    # Ensure processed data exists
    processed_file = "socials_data/personalities/aristotle/processed/data.jsonl"
    assert os.path.exists(processed_file), "Processed data file not found"

    # Load dataset
    ds = load_dataset("aristotle")
    assert len(ds) > 0, "Dataset should not be empty"

    # Check for content from each book
    content = [sample["text"] for sample in ds]
    full_text = " ".join(content)

    # Check for key phrases from the texts
    assert "moral choice" in full_text or "happiness" in full_text # Nicomachean Ethics
    assert "city is a society" in full_text or "political society" in full_text # Politics
    assert "Tragedy" in full_text or "Epic poetry" in full_text # Poetics

    # Negative assertion: Ensure Gutenberg headers are gone
    # Note: We found "START OF THE PROJECT" in raw files, checking if they are in processed
    # Be careful, sometimes small artifacts remain, but the main header should be gone.
    # We stripped explicitly using our script.

    # Our cleaning script kept from specific markers.
    # Let's check for the license text which usually appears at the start/end
    assert "Project Gutenberg License" not in full_text[:5000], "Header artifact found at start"
    assert "Project Gutenberg License" not in full_text[-5000:], "Footer artifact found at end"

if __name__ == "__main__":
    pytest.main([__file__])
