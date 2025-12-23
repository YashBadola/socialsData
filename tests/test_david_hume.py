
import pytest
import os
from socials_data.core.loader import load_dataset
from socials_data.core.manager import PersonalityManager

def test_david_hume_metadata():
    manager = PersonalityManager()
    metadata = manager.get_metadata("david_hume")
    assert metadata["name"] == "David Hume"
    assert "A Treatise of Human Nature" in [s["title"] for s in metadata["sources"]]

def test_david_hume_files_exist():
    base_path = "socials_data/personalities/david_hume"
    assert os.path.exists(os.path.join(base_path, "raw", "a_treatise_of_human_nature.txt"))
    assert os.path.exists(os.path.join(base_path, "processed", "data.jsonl"))

def test_load_dataset_david_hume():
    # Test loading the dataset
    ds = load_dataset("david_hume")
    assert len(ds) > 0
    # Check a sample
    sample = ds[0]
    assert "text" in sample
    assert "source" in sample
    assert isinstance(sample["text"], str)
    assert len(sample["text"]) > 0
