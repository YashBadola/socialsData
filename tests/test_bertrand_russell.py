import os
import pytest
from socials_data import load_dataset

def test_bertrand_russell_load_dataset():
    """Test that the Bertrand Russell dataset loads correctly."""
    dataset = load_dataset("bertrand_russell")
    assert dataset is not None, "Dataset should not be None"
    assert len(dataset) > 0, "Dataset should not be empty"

    # Check that we have the expected columns
    sample = dataset[0]
    assert "text" in sample
    assert "source" in sample

    # Verify sources
    sources = set(dataset["source"])
    expected_sources = {
        "the_problems_of_philosophy.txt",
        "the_analysis_of_mind.txt",
        "mysticism_and_logic.txt"
    }
    # It's possible not all chunks appear if they are merged, but with huge texts, we expect all to be present
    # unless the processor merged everything into one (which it does for raw text currently).
    # The memory says "The TextDataProcessor currently returns the entire cleaned text as a single chunk... without splitting it."
    # So we should have exactly 3 entries if that's true, or more if it changed.
    # Let's check if all expected sources are present.
    assert expected_sources.issubset(sources), f"Missing sources. Found: {sources}"

def test_bertrand_russell_content():
    """Test that the content is actually from Bertrand Russell."""
    dataset = load_dataset("bertrand_russell")

    # Check for specific keywords or phrases
    problems_text = next(d["text"] for d in dataset if d["source"] == "the_problems_of_philosophy.txt")
    assert "appearance and reality" in problems_text.lower(), "Content missing from Problems of Philosophy"

    analysis_text = next(d["text"] for d in dataset if d["source"] == "the_analysis_of_mind.txt")
    assert "consciousness" in analysis_text.lower(), "Content missing from Analysis of Mind"

    mysticism_text = next(d["text"] for d in dataset if d["source"] == "mysticism_and_logic.txt")
    assert "mysticism" in mysticism_text.lower(), "Content missing from Mysticism and Logic"

def test_no_gutenberg_artifacts():
    """Test that Gutenberg artifacts are removed."""
    dataset = load_dataset("bertrand_russell")
    for row in dataset:
        text = row["text"]
        assert "Project Gutenberg" not in text, f"Gutenberg artifact found in {row['source']}"
        assert "START OF THE PROJECT GUTENBERG" not in text
        assert "END OF THE PROJECT GUTENBERG" not in text
