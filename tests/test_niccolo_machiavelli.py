import pytest
from socials_data.core.loader import load_dataset
from socials_data.core.manager import PersonalityManager
from datasets import Dataset

def test_load_machiavelli_dataset():
    """Test that the Niccolò Machiavelli dataset loads correctly."""
    dataset = load_dataset("niccolo_machiavelli")

    assert isinstance(dataset, Dataset)
    assert len(dataset) > 10  # Should be many chunks

    # Check columns
    assert "text" in dataset.column_names
    assert "source" in dataset.column_names

    # Verify content
    # We expect content from The Prince and Discourses

    # Convert to list for searching
    texts = dataset["text"]
    sources = dataset["source"]

    # Check for specific keywords
    keywords = ["virtu", "fortune", "prince", "republic", "Machiavelli"]
    found_keywords = {k: False for k in keywords}

    for text in texts:
        for k in keywords:
            if k.lower() in text.lower():
                found_keywords[k] = True

    # We expect most keywords to be found across the corpus
    assert found_keywords["prince"], "The word 'prince' was not found in the dataset."
    assert found_keywords["fortune"], "The word 'fortune' was not found in the dataset."

    # Verify sources
    unique_sources = set(sources)
    assert "the_prince.txt" in unique_sources
    assert "discourses_on_livy.txt" in unique_sources

def test_machiavelli_metadata():
    """Test that metadata is correctly configured."""
    manager = PersonalityManager()
    metadata = manager.get_metadata("niccolo_machiavelli")

    assert metadata["name"] == "Niccolò Machiavelli"
    assert "pragmatic realist" in metadata["system_prompt"]
    assert len(metadata["sources"]) == 2
