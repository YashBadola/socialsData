import os
import pytest
from socials_data.core.loader import load_dataset
from socials_data.core.manager import PersonalityManager

def test_load_dataset_david_hume():
    """
    Test that the David Hume dataset loads correctly and contains valid data.
    """
    dataset = load_dataset("david_hume")
    assert dataset is not None
    assert len(dataset) > 0

    # Check the first few samples
    # Slice returns a dictionary of lists: {'text': [...], 'source': [...]}
    sample_batch = dataset[:5]

    assert "text" in sample_batch
    assert "source" in sample_batch

    texts = sample_batch["text"]
    sources = sample_batch["source"]

    # We expect at least 5 chunks now
    assert len(texts) == 5
    assert len(sources) == 5

    for text in texts:
        assert isinstance(text, str)
        assert len(text) > 0

    for source in sources:
        assert isinstance(source, str)
        assert source.endswith(".txt")

def test_metadata_david_hume():
    """
    Test that the metadata for David Hume is correct.
    """
    manager = PersonalityManager()
    metadata = manager.get_metadata("david_hume")

    assert metadata["name"] == "David Hume"
    assert "system_prompt" in metadata
    assert len(metadata["sources"]) == 2
    assert metadata["sources"][0]["title"] == "An Enquiry Concerning Human Understanding"
    assert metadata["sources"][1]["title"] == "A Treatise of Human Nature"

def test_content_keywords_david_hume():
    """
    Test that the content actually resembles Hume's writing (basic keyword check).
    """
    dataset = load_dataset("david_hume")

    # Check a larger batch for keywords
    texts = dataset[:100]["text"]
    full_text = " ".join(texts).lower()

    keywords = ["impression", "idea", "reason", "nature", "cause", "effect"]
    for keyword in keywords:
        assert keyword in full_text, f"Keyword '{keyword}' not found in the first 100 chunks."
