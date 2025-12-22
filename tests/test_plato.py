import pytest
from socials_data.core.loader import load_dataset
from socials_data.core.manager import PersonalityManager
from datasets import Dataset

def test_plato_dataset_loading():
    """Test that the Plato dataset can be loaded correctly."""
    dataset = load_dataset("plato")
    assert isinstance(dataset, Dataset)
    assert len(dataset) > 0

    # Check first few samples for content
    sample = dataset[0]
    assert "text" in sample
    assert "source" in sample
    assert isinstance(sample["text"], str)
    assert len(sample["text"]) > 0

def test_plato_metadata():
    """Test that Plato metadata is correct."""
    manager = PersonalityManager()
    metadata = manager.get_metadata("plato")
    assert metadata["name"] == "Plato"
    assert "The Republic" in [s["title"] for s in metadata["sources"]]
    assert "You are Plato" in metadata["system_prompt"]

def test_plato_content_keywords():
    """Test that the content contains expected keywords."""
    dataset = load_dataset("plato")

    # Check for keywords across a subset of data
    keywords = ["Socrates", "justice", "soul", "virtue", "state"]
    found_keywords = {k: False for k in keywords}

    for i in range(min(len(dataset), 100)):
        text = dataset[i]["text"]
        for k in keywords:
            if k in text:
                found_keywords[k] = True

    # We expect at least some of these to be found in the first 100 chunks
    assert any(found_keywords.values()), f"None of the keywords {keywords} found in the first 100 chunks."
