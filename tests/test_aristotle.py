
import pytest
from socials_data.core.loader import load_dataset
from socials_data.core.manager import PersonalityManager

def test_aristotle_dataset_loading():
    """Test that the Aristotle dataset loads correctly."""
    dataset = load_dataset("aristotle")
    assert dataset is not None, "Dataset should not be None"
    assert len(dataset) > 0, "Dataset should not be empty"

    # Check schema
    sample = dataset[0]
    assert "text" in sample
    assert "source" in sample
    assert isinstance(sample["text"], str)
    assert isinstance(sample["source"], str)

def test_aristotle_content_relevance():
    """Test that the content contains expected keywords."""
    dataset = load_dataset("aristotle")

    # Slicing a HF dataset returns a dict of lists
    text_corpus = " ".join(dataset[:50]["text"])

    keywords = ["virtue", "state", "good", "political", "nature", "mean", "happiness"]
    found_any = any(keyword in text_corpus.lower() for keyword in keywords)

    assert found_any, f"Expected to find at least one of {keywords} in the first 50 samples"

def test_aristotle_sources():
    """Test that the sources are correctly attributed."""
    dataset = load_dataset("aristotle")
    sources = set(d["source"] for d in dataset)

    # We expect filenames to be the source
    expected_sources = {"nicomachean_ethics.txt", "politics.txt"}
    assert sources.intersection(expected_sources), f"Expected sources from {expected_sources}, but got {sources}"
