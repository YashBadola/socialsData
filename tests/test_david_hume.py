import os
import pytest
from socials_data.core.loader import load_dataset
from socials_data.core.manager import PersonalityManager

def test_load_dataset_david_hume():
    # Verify the personality exists in the manager
    manager = PersonalityManager()
    personalities = manager.list_personalities()
    assert "david_hume" in personalities

    # Load the dataset
    dataset = load_dataset("david_hume")

    # Check that it returns a Hugging Face Dataset
    from datasets import Dataset
    assert isinstance(dataset, Dataset)

    # Check that it has data
    assert len(dataset) > 0

    # Check samples
    sample = dataset[0]
    assert "text" in sample
    assert "source" in sample
    assert isinstance(sample["text"], str)
    assert len(sample["text"]) > 0

    # Check content relevance (look for keywords)
    # Since we have two books, we check for a few keywords that should be present in the whole dataset
    # We scan a few samples to find these keywords.

    found_hume_keywords = False
    keywords = ["idea", "impression", "reason", "passion", "cause", "effect"]

    # Check first 100 samples or all if less
    for i in range(min(len(dataset), 100)):
        text = dataset[i]["text"].lower()
        if any(k in text for k in keywords):
            found_hume_keywords = True
            break

    assert found_hume_keywords, "Did not find expected Hume keywords in the first 100 samples"

    # Verify sources
    unique_sources = set(dataset["source"])
    assert "a_treatise_of_human_nature.txt" in unique_sources
    assert "an_enquiry_concerning_human_understanding.txt" in unique_sources

def test_metadata_david_hume():
    manager = PersonalityManager()
    metadata = manager.get_metadata("david_hume")

    assert metadata["name"] == "David Hume"
    assert metadata["id"] == "david_hume"
    assert "empiricism" in metadata["description"].lower()
    assert len(metadata["sources"]) == 2
