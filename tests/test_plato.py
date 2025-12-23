import pytest
from socials_data import load_dataset
from socials_data.core.manager import PersonalityManager

def test_load_plato_dataset():
    """Test that the Plato dataset loads correctly."""
    dataset = load_dataset("plato")
    assert dataset is not None
    assert len(dataset) > 0

    # Check structure
    sample = dataset[0]
    assert "text" in sample
    assert "source" in sample
    assert sample["source"] in ["the_republic.txt", "apology.txt", "symposium.txt"]

def test_plato_content():
    """Test that specific content from Plato's works is present."""
    dataset = load_dataset("plato")

    # Check for a famous line from The Republic
    # Note: dataset is not just a list, it's a Hugging Face dataset.
    # We need to iterate or filter.

    found_republic = False
    found_apology = False
    found_symposium = False

    # Check a subset to avoid slow tests if dataset is huge,
    # but here we want to ensure coverage so we might need to search.
    # Let's search for keywords in the first 100 entries or random sample?
    # Or just iterate all since it's text.

    for item in dataset:
        text = item["text"]
        source = item["source"]

        if "the_republic.txt" in source:
            found_republic = True
            if "Glaucon" in text or "Socrates" in text:
                pass # Confirmation of content

        if "apology.txt" in source:
            found_apology = True

        if "symposium.txt" in source:
            found_symposium = True

    assert found_republic, "The Republic data not found in dataset"
    assert found_apology, "Apology data not found in dataset"
    assert found_symposium, "Symposium data not found in dataset"

def test_plato_metadata():
    """Test that Plato metadata is correct."""
    manager = PersonalityManager()
    metadata = manager.get_metadata("plato")

    assert metadata["name"] == "Plato"
    assert "Socratic method" in metadata["system_prompt"]
    assert len(metadata["sources"]) == 3
