import os
import pytest
from socials_data.core.manager import PersonalityManager
from socials_data import load_dataset
from datasets import Dataset

def test_load_schopenhauer_dataset():
    # Load the dataset
    dataset = load_dataset("arthur_schopenhauer")

    # Check if it returns a Dataset object
    assert isinstance(dataset, Dataset)

    # Check if it's not empty
    assert len(dataset) > 0

    # Check the columns
    assert "text" in dataset.column_names
    assert "source" in dataset.column_names

    # Check a sample
    sample = dataset[0]
    assert isinstance(sample["text"], str)
    assert len(sample["text"]) > 0

    # Verify sources are correct
    sources = set(dataset["source"])
    assert "world_as_will_vol1.txt" in sources
    assert "essays_of_schopenhauer.txt" in sources
    assert "counsels_and_maxims.txt" in sources

def test_schopenhauer_metadata():
    pm = PersonalityManager()
    metadata = pm.get_metadata("arthur_schopenhauer")

    assert metadata["name"] == "Arthur Schopenhauer"
    assert metadata["id"] == "arthur_schopenhauer"
    assert "pessimistic" in metadata["system_prompt"].lower()
    assert len(metadata["sources"]) >= 3
