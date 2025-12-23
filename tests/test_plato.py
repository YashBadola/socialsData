import os
import pytest
from socials_data.core.loader import load_dataset
from socials_data.core.manager import PersonalityManager

def test_load_plato_dataset():
    """Test that the Plato dataset loads correctly."""
    dataset = load_dataset("plato")

    # Check that we got a Dataset object
    assert hasattr(dataset, "column_names")
    assert "text" in dataset.column_names
    assert "source" in dataset.column_names

    # Check that we have data
    assert len(dataset) > 0

    # Verify content of a sample
    sample = dataset[0]
    assert isinstance(sample["text"], str)
    assert len(sample["text"]) > 0

    # Verify sources are correct
    # We sliced slicing logic in the test: dataset[:5]["source"] returns a list of sources
    sources = set(dataset[:10]["source"])
    assert any("the_republic.txt" in s for s in sources) or any("symposium.txt" in s for s in sources)

def test_plato_metadata():
    """Test that Plato metadata is correct."""
    manager = PersonalityManager()
    metadata = manager.get_metadata("plato")

    assert metadata["name"] == "Plato"
    assert metadata["id"] == "plato"
    assert "The Republic" in [s["title"] for s in metadata["sources"]]
    assert metadata["license"] == "Public Domain"

def test_plato_content_keywords():
    """Test that the content actually looks like Plato."""
    dataset = load_dataset("plato")

    # Concatenate first few entries to check for keywords
    text_sample = " ".join(dataset[:20]["text"]).lower()

    # Keywords that should likely appear in the first few chunks of Republic or Symposium
    keywords = ["socrates", "justice", "good", "truth", "dialogue", "speech", "nature", "man", "state"]

    found_keywords = [k for k in keywords if k in text_sample]
    assert len(found_keywords) > 0, f"Expected to find some Plato keywords in: {text_sample[:500]}..."
