
import pytest
import os
from socials_data.core.manager import PersonalityManager
from socials_data import load_dataset
from datasets import Dataset

@pytest.fixture
def manager():
    return PersonalityManager()

def test_load_dataset_immanuel_kant(manager):
    # Verify metadata
    metadata = manager.get_metadata("immanuel_kant")
    assert metadata["name"] == "Immanuel Kant"
    assert metadata["id"] == "immanuel_kant"
    assert len(metadata["sources"]) >= 2

    # Load dataset
    dataset = load_dataset("immanuel_kant")

    # Verify it returns a Dataset object
    assert isinstance(dataset, Dataset)

    # Verify content
    assert len(dataset) > 0

    # Check a sample
    sample = dataset[0]
    assert "text" in sample
    assert "source" in sample
    assert isinstance(sample["text"], str)
    assert len(sample["text"]) > 0

    # Verify sources are present in the dataset
    sources = set(dataset["source"])
    assert "critique_of_pure_reason.txt" in sources
    assert "critique_of_practical_reason.txt" in sources

    # Simple content check
    # We expect words like "reason", "pure", "practical" to appear in the text
    text_content = " ".join(dataset[:10]["text"]).lower()
    assert "reason" in text_content
    assert "pure" in text_content or "practical" in text_content

def test_immanuel_kant_metadata_integrity(manager):
    metadata = manager.get_metadata("immanuel_kant")
    assert "system_prompt" in metadata
    assert "You are Immanuel Kant" in metadata["system_prompt"]
