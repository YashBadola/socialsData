import pytest
from socials_data import load_dataset
from socials_data.core.manager import PersonalityManager
from pathlib import Path
import json

def test_load_plato_dataset():
    """Verify that the Plato dataset loads correctly using load_dataset."""
    dataset = load_dataset("plato")

    # Check if we got a dataset
    assert dataset is not None
    assert len(dataset) > 0

    # Check sample structure
    sample = dataset[0]
    assert "text" in sample
    assert "source" in sample
    assert isinstance(sample["text"], str)
    assert len(sample["text"]) > 0

    # Verify sources
    sources = set(dataset["source"])
    expected_sources = {"the_republic.txt", "apology_crito_phaedo.txt", "symposium.txt"}
    # Note: Depending on processing, not all chunks might appear if files are small (unlikely)
    # or if errors occurred, but for Plato we expect all.
    assert expected_sources.issubset(sources)

    # Check for some keywords in text to ensure content is correct
    all_text = " ".join(dataset["text"][:10]) # Check first 10 chunks
    keywords = ["Socrates", "virtue", "justice", "truth", "God", "Athens"]

    found_any = any(k in all_text for k in keywords)
    assert found_any, f"Did not find expected keywords in the first 10 chunks. Text sample: {all_text[:200]}"

def test_plato_metadata():
    """Verify metadata integrity for Plato."""
    base_dir = Path("socials_data/personalities")
    manager = PersonalityManager(base_dir)
    metadata = manager.get_metadata("plato")

    assert metadata["name"] == "Plato"
    assert metadata["id"] == "plato"
    assert "Socratic method" in metadata["system_prompt"]
    assert len(metadata["sources"]) == 3
