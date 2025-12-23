import os
import pytest
from socials_data.core.manager import PersonalityManager
from socials_data.core.loader import load_dataset
from datasets import Dataset

@pytest.fixture
def manager():
    return PersonalityManager()

def test_schopenhauer_metadata(manager):
    meta = manager.get_metadata("arthur_schopenhauer")
    assert meta["name"] == "Arthur Schopenhauer"
    assert "World as Will" in meta["description"] or "World as Will" in meta["system_prompt"]
    assert len(meta["sources"]) == 3

def test_schopenhauer_dataset_loading():
    # Test loading via the manager or loader
    ds = load_dataset("arthur_schopenhauer")
    assert isinstance(ds, Dataset)
    assert len(ds) > 10

    # Check a sample
    sample = ds[0]
    assert "text" in sample
    assert "source" in sample
    assert isinstance(sample["text"], str)
    assert len(sample["text"]) > 0

    # Verify content relevance (keyword check)
    # Check for common Schopenhauer terms in the whole dataset
    all_text = " ".join([d["text"] for d in ds])
    keywords = ["will", "suffering", "existence", "intellect", "fame", "controversy"]
    found = [k for k in keywords if k in all_text.lower()]
    assert len(found) > 0, "No Schopenhauer keywords found in the dataset"

def test_schopenhauer_sources_in_dataset():
    ds = load_dataset("arthur_schopenhauer")
    sources = set(ds["source"])
    expected_sources = {"wisdom_of_life.txt", "art_of_controversy.txt", "essays_of_schopenhauer.txt"}

    # Check if we have ALL expected sources
    missing_sources = expected_sources - sources
    assert not missing_sources, f"Missing sources: {missing_sources}"
