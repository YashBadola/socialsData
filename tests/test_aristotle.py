import json
from pathlib import Path
from socials_data.core.manager import PersonalityManager
from socials_data import load_dataset as main_load_dataset

def test_aristotle_personality_exists():
    """Test that Aristotle exists in the personality manager."""
    manager = PersonalityManager()
    personalities = manager.list_personalities()
    assert "aristotle" in personalities

def test_aristotle_metadata():
    """Test that Aristotle's metadata is correct."""
    manager = PersonalityManager()
    metadata = manager.get_metadata("aristotle")

    assert metadata["name"] == "Aristotle"
    assert metadata["id"] == "aristotle"
    assert len(metadata["sources"]) == 3
    assert "Nicomachean Ethics" in [s["title"] for s in metadata["sources"]]
    assert "Politics" in [s["title"] for s in metadata["sources"]]
    assert "Poetics" in [s["title"] for s in metadata["sources"]]

def test_aristotle_dataset_loading():
    """Test that the Aristotle dataset loads correctly."""
    dataset = main_load_dataset("aristotle")
    assert len(dataset) > 0

    # Check first item structure
    item = dataset[0]
    assert "text" in item
    assert "source" in item

    # Check sources are present in the data
    sources = set(dataset["source"])
    assert "nicomachean_ethics.txt" in sources
    assert "politics.txt" in sources
    assert "poetics.txt" in sources

def test_aristotle_content_samples():
    """Test specific content presence to verify data integrity."""
    dataset = main_load_dataset("aristotle")

    # Check for famous concepts
    text_content = " ".join(dataset["text"])

    # We might need to handle case sensitivity, so we lower it
    text_content_lower = text_content.lower()

    assert "virtue" in text_content_lower
    assert "happiness" in text_content_lower or "eudaimonia" in text_content_lower
    assert "state" in text_content_lower or "polis" in text_content_lower
    assert "tragedy" in text_content_lower # From Poetics
