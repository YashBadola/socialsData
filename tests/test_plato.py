import os
import json
import pytest
from pathlib import Path
from socials_data.core.loader import load_dataset
from socials_data.core.manager import PersonalityManager

def test_plato_dataset_loading():
    """Verify that the Plato dataset can be loaded correctly."""
    dataset = load_dataset("plato")

    # Check that it returns a Dataset object
    assert hasattr(dataset, "features"), "Should return a Hugging Face Dataset"
    assert len(dataset) > 0, "Dataset should not be empty"

    # Check columns
    assert "text" in dataset.features
    assert "source" in dataset.features

def test_plato_content_checks():
    """Verify that the content contains expected strings."""
    dataset = load_dataset("plato")

    # Convert to list for easier searching
    texts = [item["text"] for item in dataset]
    sources = set([item["source"] for item in dataset])

    # Verify sources
    expected_sources = {"the_republic.txt", "symposium.txt", "apology_crito_phaedo.txt", "phaedrus.txt"}
    assert sources.issubset(expected_sources), f"Found unexpected sources: {sources - expected_sources}"
    assert expected_sources.issubset(sources), f"Missing sources: {expected_sources - sources}"

    # Verify specific content fragments (using keywords relevant to Plato)
    combined_text = " ".join(texts).lower()

    keywords = ["socrates", "philosopher", "justice", "truth", "soul", "dialogue", "athens"]
    for keyword in keywords:
        assert keyword in combined_text, f"Keyword '{keyword}' not found in dataset"

def test_metadata_integrity():
    """Verify metadata.json structure and content."""
    manager = PersonalityManager()
    metadata = manager.get_metadata("plato")

    assert metadata["name"] == "Plato"
    assert metadata["id"] == "plato"
    assert "system_prompt" in metadata
    assert len(metadata["sources"]) == 4

def test_no_gutenberg_artifacts():
    """Verify that common Gutenberg artifacts are removed."""
    dataset = load_dataset("plato")
    combined_text = " ".join([item["text"] for item in dataset])

    artifacts = [
        "*** START OF THE PROJECT GUTENBERG EBOOK",
        "*** END OF THE PROJECT GUTENBERG EBOOK",
        "Project Gutenberg License",
        "START OF THIS PROJECT GUTENBERG EBOOK"
    ]

    for artifact in artifacts:
        assert artifact not in combined_text, f"Artifact '{artifact}' found in text"

if __name__ == "__main__":
    pytest.main([__file__])
