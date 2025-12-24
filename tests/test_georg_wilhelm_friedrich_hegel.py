import os
import pytest
from socials_data import load_dataset
from socials_data.core.manager import PersonalityManager

def test_hegel_dataset_structure():
    """Test that the Hegel dataset can be loaded and has correct structure."""
    dataset = load_dataset("georg_wilhelm_friedrich_hegel")

    # Check that it returns a Dataset object (not a dict split)
    assert hasattr(dataset, "column_names")
    assert "text" in dataset.column_names
    assert "source" in dataset.column_names

    # Check length (we have 4 sources)
    # The processor currently merges file content into one chunk per file?
    # Or splits? Memory says "returns the entire cleaned text as a single chunk in processed/data.jsonl, without splitting it."
    # So we should have exactly 4 rows.
    assert len(dataset) == 4

def test_hegel_content():
    """Test specific content in the Hegel dataset."""
    dataset = load_dataset("georg_wilhelm_friedrich_hegel")

    # Check that sources are correct
    sources = set(dataset["source"])
    expected_sources = {
        "philosophy_of_mind.txt",
        "logic_of_hegel.txt",
        "lectures_history_philosophy_v1.txt",
        "philosophy_of_fine_art_v1.txt"
    }
    assert sources == expected_sources

    # Check content in Philosophy of Mind
    mind_text = next(item["text"] for item in dataset if item["source"] == "philosophy_of_mind.txt")
    assert "THE PHILOSOPHY OF MIND" in mind_text or "SECTION I" in mind_text or "mind" in mind_text.lower()
    assert "Project Gutenberg" not in mind_text  # Should be cleaned out?
    # Wait, my cleaning script dumped the cleaned text into raw/filename.txt.
    # The clean_text function used slicing: text[start_idx:end_idx].
    # The end marker was "End of the Project Gutenberg EBook".
    # So the footer should be gone.
    # The start marker was kept.
    # But does the start marker *precede* the license header?
    # Yes, "THE PHILOSOPHY OF MIND" is usually after the header.

    # Check logic
    logic_text = next(item["text"] for item in dataset if item["source"] == "logic_of_hegel.txt")
    assert len(logic_text) > 1000

def test_metadata():
    """Test metadata loading."""
    manager = PersonalityManager()
    metadata = manager.get_metadata("georg_wilhelm_friedrich_hegel")

    assert metadata["name"] == "Georg Wilhelm Friedrich Hegel"
    assert len(metadata["sources"]) == 4
