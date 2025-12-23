import json
import pytest
from pathlib import Path
from socials_data import load_dataset
from socials_data.core.manager import PersonalityManager

def test_david_hume_metadata():
    """Test that metadata loads correctly."""
    manager = PersonalityManager()
    metadata = manager.get_metadata("david_hume")

    assert metadata["name"] == "David Hume"
    assert metadata["id"] == "david_hume"
    assert "Enlightenment" in metadata["description"]
    assert len(metadata["sources"]) >= 2

def test_david_hume_dataset_loading():
    """Test loading the processed dataset."""
    dataset = load_dataset("david_hume")

    # Check that we have data
    assert len(dataset) > 0

    # Check content of a sample
    sample = dataset[0]
    assert "text" in sample
    assert "source" in sample
    assert isinstance(sample["text"], str)
    assert len(sample["text"]) > 0

def test_david_hume_content_relevance():
    """Test that the content actually looks like Hume."""
    dataset = load_dataset("david_hume")

    # Scan a few samples for key terms
    found_keywords = False
    keywords = ["impression", "idea", "cause", "effect", "reason", "passion", "understanding", "nature"]

    for i in range(min(100, len(dataset))):
        text = dataset[i]["text"].lower()
        if any(keyword in text for keyword in keywords):
            found_keywords = True
            break

    assert found_keywords, "Did not find expected Humean keywords in the first 100 samples"

def test_source_attribution():
    """Test that sources are correctly attributed."""
    dataset = load_dataset("david_hume")
    sources = set(dataset["source"])

    # Based on our download script, filenames should be in the sources
    assert "treatise_of_human_nature.txt" in sources or "enquiry_human_understanding.txt" in sources
