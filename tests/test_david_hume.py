import os
import pytest
from socials_data.core.manager import PersonalityManager
from socials_data import load_dataset

def test_david_hume_dataset_exists():
    manager = PersonalityManager()
    personalities = manager.list_personalities()
    assert "david_hume" in personalities

def test_david_hume_metadata():
    manager = PersonalityManager()
    metadata = manager.get_metadata("david_hume")
    assert metadata["name"] == "David Hume"
    assert "skeptic" in metadata["system_prompt"]
    assert len(metadata["sources"]) == 2

def test_david_hume_load_dataset():
    dataset = load_dataset("david_hume")
    # Check that it returns a Hugging Face Dataset
    assert dataset is not None
    # Check that it has data
    assert len(dataset) > 0
    # Check the first sample
    sample = dataset[0]
    assert "text" in sample
    assert "source" in sample
    assert isinstance(sample["text"], str)
    assert len(sample["text"]) > 0

def test_david_hume_content_check():
    dataset = load_dataset("david_hume")
    # Convert to list to iterate
    samples = list(dataset)

    # Check for keywords from the texts
    has_treatise_content = False
    has_enquiry_content = False

    for sample in samples:
        text = sample["text"].lower()
        if "treatise" in sample["source"].lower() or "treatise" in text:
             has_treatise_content = True
        if "enquiry" in sample["source"].lower() or "enquiry" in text or "impression" in text or "idea" in text:
             has_enquiry_content = True

    # Since we loaded specific files, we can just check if we have data from them.
    # The source field in processed/data.jsonl contains the filename.
    sources = set([s["source"] for s in samples])
    assert "treatise_human_nature.txt" in sources
    assert "enquiry_human_understanding.txt" in sources
