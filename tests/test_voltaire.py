import os
import pytest
from socials_data.core.loader import load_dataset
from socials_data.core.manager import PersonalityManager

def test_voltaire_dataset_loads():
    """Verify that the Voltaire dataset loads correctly."""
    dataset = load_dataset("voltaire")
    assert len(dataset) > 0, "Dataset should not be empty"

    # Check schema
    sample = dataset[0]
    assert "text" in sample, "Sample should have a 'text' field"
    assert "source" in sample, "Sample should have a 'source' field"
    assert isinstance(sample["text"], str), "Text should be a string"
    assert len(sample["text"]) > 0, "Text should not be empty"

def test_voltaire_content_integrity():
    """Check for expected content and absence of Gutenberg artifacts."""
    dataset = load_dataset("voltaire")

    found_candide = False
    found_zadig = False
    found_micromegas = False

    for item in dataset:
        text = item["text"]
        source = item["source"]

        # Check for specific quotes or keywords
        if "Candide" in source or "candide" in source:
            found_candide = True
            # "best of all possible worlds" is a famous phrase
            if "best of all possible worlds" in text.lower():
                pass

        if "Zadig" in source or "zadig" in source:
            found_zadig = True

        if "Micromegas" in source or "micromegas" in source:
            found_micromegas = True

        # Negative assertions for Gutenberg artifacts
        assert "Project Gutenberg" not in text, f"Found Gutenberg artifact in {source}"
        assert "START OF THE PROJECT" not in text, f"Found start marker in {source}"
        assert "END OF THE PROJECT" not in text, f"Found end marker in {source}"

    # Note: Depending on chunking, we might not find specific phrases in *every* chunk,
    # but we should at least have data from the sources.
    assert found_candide, "Should have content from Candide"
    assert found_zadig, "Should have content from Zadig"
    assert found_micromegas, "Should have content from Micromegas"

def test_voltaire_metadata():
    """Verify metadata is correct."""
    manager = PersonalityManager()
    metadata = manager.get_metadata("voltaire")

    assert metadata["name"] == "Voltaire"
    assert "François-Marie Arouet" in metadata["description"]
    assert "Candide" in [s["title"] for s in metadata["sources"]]
