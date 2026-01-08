import pytest
from socials_data import load_dataset
from socials_data.core.manager import PersonalityManager
import json
from pathlib import Path

def test_plato_dataset_loading():
    """
    Test that the Plato dataset can be loaded via the load_dataset function.
    """
    try:
        dataset = load_dataset("plato")
    except Exception as e:
        pytest.fail(f"Failed to load dataset: {e}")

    assert len(dataset) > 0, "Dataset should not be empty"

    # Check schema
    assert "text" in dataset.column_names
    assert "source" in dataset.column_names

    # Check content of a sample
    sample = dataset[0]
    assert isinstance(sample["text"], str)
    assert len(sample["text"]) > 100

    # Check that source is one of the expected files
    expected_sources = ["republic.txt", "apology_crito_phaedo.txt", "symposium.txt"]
    assert sample["source"] in expected_sources

def test_plato_metadata():
    """
    Test that the metadata for Plato is correct.
    """
    manager = PersonalityManager()
    metadata = manager.get_metadata("plato")

    assert metadata["name"] == "Plato"
    assert "Socratic" in metadata["system_prompt"]
    assert len(metadata["sources"]) == 3
    assert metadata["license"] == "Public Domain"

def test_plato_content_keywords():
    """
    Test that the content actually looks like Plato (contains specific keywords).
    """
    dataset = load_dataset("plato")

    # Concatenate a few samples to check for keywords
    # Note: dataset slicing returns a dict of lists
    texts = dataset[:5]["text"]
    combined_text = " ".join(texts).lower()

    keywords = ["socrates", "philosophy", "virtue", "athens", "truth"]
    for keyword in keywords:
        assert keyword in combined_text, f"Keyword '{keyword}' not found in the first few samples"

if __name__ == "__main__":
    pytest.main([__file__])
