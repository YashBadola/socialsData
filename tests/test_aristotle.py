import pytest
import os
import json
from socials_data.core.manager import PersonalityManager
from datasets import Dataset

@pytest.fixture
def manager():
    return PersonalityManager()

def test_aristotle_personality_exists(manager):
    personalities = manager.list_personalities()
    assert "aristotle" in personalities

def test_aristotle_metadata(manager):
    metadata = manager.get_metadata("aristotle")
    assert metadata["name"] == "Aristotle"
    assert metadata["id"] == "aristotle"
    assert "System" in metadata["system_prompt"] or "Aristotle" in metadata["system_prompt"]
    assert len(metadata["sources"]) >= 3

    titles = [s["title"] for s in metadata["sources"]]
    assert "The Nicomachean Ethics" in titles
    assert "Politics" in titles
    assert "Poetics" in titles

def test_aristotle_raw_files_exist(manager):
    # Manually check paths since manager might not expose get_raw_dir
    base_dir = manager.base_dir
    raw_dir = base_dir / "aristotle" / "raw"

    assert (raw_dir / "nicomachean_ethics.txt").exists()
    assert (raw_dir / "politics.txt").exists()
    assert (raw_dir / "poetics.txt").exists()

def test_aristotle_dataset_loading():
    # We use the direct loading function or the manager if it has it
    from socials_data import load_dataset

    ds = load_dataset("aristotle")
    assert isinstance(ds, Dataset)
    assert len(ds) > 100 # Should be plenty of chunks

    # Check a sample
    sample = ds[0]
    assert "text" in sample
    assert "source" in sample
    assert isinstance(sample["text"], str)
    assert len(sample["text"]) > 0

def test_aristotle_content_relevance():
    from socials_data import load_dataset
    ds = load_dataset("aristotle")

    # Check for keywords in the text to ensure we loaded the right stuff
    text_content = " ".join(ds[:20]["text"])

    keywords = ["virtue", "state", "poetry", "politics", "happiness", "tragedy"]
    found = [k for k in keywords if k in text_content.lower()]

    # We expect at least some of these to be present in the first few chunks
    # (Note: ordering might vary, but with 20 chunks we should hit something)
    assert len(found) > 0
