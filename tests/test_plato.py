import pytest
import json
import os
from pathlib import Path
from socials_data import load_dataset
from socials_data.core.manager import PersonalityManager

def test_plato_dataset_loading():
    """Test that the Plato dataset can be loaded via load_dataset."""
    # Ensure processed file exists
    processed_path = Path("socials_data/personalities/plato/processed/data.jsonl")
    assert processed_path.exists(), "Processed data file not found"

    # Load dataset
    ds = load_dataset("plato")
    assert len(ds) > 0, "Dataset should not be empty"

    # Check first sample
    sample = ds[0]
    assert "text" in sample
    assert "source" in sample
    assert isinstance(sample["text"], str)
    assert len(sample["text"]) > 0

def test_plato_metadata():
    """Test that Plato's metadata is correct."""
    manager = PersonalityManager()
    metadata = manager.get_metadata("plato")

    assert metadata["name"] == "Plato"
    assert metadata["id"] == "plato"
    assert "The Republic" in [s["title"] for s in metadata["sources"]]
    assert metadata["system_prompt"].startswith("You are Plato.")

def test_plato_content_relevance():
    """Test that the content actually resembles Plato's texts."""
    ds = load_dataset("plato")

    # Keywords we expect in Plato's works
    keywords = ["Socrates", "virtue", "justice", "soul", "state", "truth"]

    found_keywords = {k: False for k in keywords}

    # Check first 50 samples or so
    for i in range(min(len(ds), 50)):
        text = ds[i]["text"]
        for k in keywords:
            if k in text or k.lower() in text.lower():
                found_keywords[k] = True

    # We expect to find at least some of these keywords
    assert any(found_keywords.values()), f"None of the keywords {keywords} found in the first 50 samples"

def test_plato_source_filenames():
    """Test that the sources are correctly attributed to filenames."""
    ds = load_dataset("plato")
    sources = set(ds["source"])

    expected_sources = {"the_republic.txt", "symposium.txt", "apology.txt"}

    # Since the dataset is chunked, we might not see all files in a small sample if we don't check all,
    # but the set of all sources should be a subset of expected sources, and ideally contain them if we check enough.
    # Actually, let's just check that every source present is valid.

    for s in sources:
        assert s in expected_sources, f"Unexpected source file: {s}"

    # Check that we have data from all 3 files
    assert expected_sources.issubset(sources), f"Missing data from sources: {expected_sources - sources}"
