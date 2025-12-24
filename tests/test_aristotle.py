import os
import pytest
from socials_data import load_dataset
from socials_data.core.manager import PersonalityManager

def test_aristotle_personality_exists():
    """Test that the Aristotle personality is correctly registered."""
    manager = PersonalityManager()
    personalities = manager.list_personalities()

    assert "aristotle" in personalities

    metadata = manager.get_metadata("aristotle")
    assert metadata["name"] == "Aristotle"
    assert "Lyceum" in metadata["description"]
    assert len(metadata["sources"]) == 5

def test_aristotle_data_loading():
    """Test that the Aristotle dataset loads correctly."""
    dataset = load_dataset("aristotle")

    # Check that we have data
    assert len(dataset) > 0

    # Check sample content
    sample = dataset[0]
    assert "text" in sample
    assert isinstance(sample["text"], str)
    assert len(sample["text"]) > 0

    # Search for characteristic terms in the dataset
    # We'll just check if we can find "virtue" or "state" or "tragedy" in the first few entries
    # slicing returns a dict of lists
    texts = dataset[:100]["text"]
    combined_text = " ".join(texts).lower()

    keywords = ["virtue", "state", "tragedy", "nature", "man"]
    # At least one keyword should be present
    assert any(keyword in combined_text for keyword in keywords)

def test_aristotle_raw_files_exist():
    """Test that the raw files were downloaded."""
    base_dir = os.path.dirname(os.path.abspath(__file__))
    raw_dir = os.path.join(base_dir, "../socials_data/personalities/aristotle/raw")

    expected_files = [
        "nicomachean_ethics.txt",
        "politics.txt",
        "poetics.txt",
        "athenian_constitution.txt",
        "categories.txt"
    ]

    for filename in expected_files:
        filepath = os.path.join(raw_dir, filename)
        assert os.path.exists(filepath), f"Missing raw file: {filename}"
        assert os.path.getsize(filepath) > 0, f"Empty raw file: {filename}"

def test_no_gutenberg_header():
    """Test that Gutenberg headers are stripped (heuristic)."""
    dataset = load_dataset("aristotle")
    texts = dataset[:50]["text"]
    combined_text = " ".join(texts)

    assert "START OF THE PROJECT GUTENBERG" not in combined_text
    # Note: "End of the Project Gutenberg" might be at the very end of the last chunk,
    # but we checked the beginning chunks.
