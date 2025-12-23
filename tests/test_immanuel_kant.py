import json
import pytest
from socials_data.core.manager import PersonalityManager
from socials_data import load_dataset as main_load_dataset

@pytest.fixture
def manager():
    return PersonalityManager()

def test_immanuel_kant_metadata(manager):
    metadata = manager.get_metadata("immanuel_kant")
    assert metadata["name"] == "Immanuel Kant"
    assert metadata["id"] == "immanuel_kant"
    assert "The Critique of Pure Reason" in [s["title"] for s in metadata["sources"]]
    assert metadata["license"] == "Public Domain"

def test_immanuel_kant_processed_data():
    dataset = main_load_dataset("immanuel_kant")
    assert len(dataset) > 0

    # Check a sample
    sample = dataset[0]
    assert "text" in sample
    assert "source" in sample
    assert isinstance(sample["text"], str)
    assert len(sample["text"]) > 0

    # Ensure content is relevant (look for keywords)
    # Since dataset is chunked, we might not find "Critique" in the first chunk,
    # but we should find something Kantian if we check enough samples or just verify the source filename.

    sources = set(dataset["source"])
    assert "critique_of_pure_reason.txt" in sources
    assert "critique_of_practical_reason.txt" in sources
    assert "critique_of_judgement.txt" in sources

    # Check for specific terms in a larger sample
    text_blob = " ".join(dataset[:20]["text"])
    assert "reason" in text_blob.lower() or "judgement" in text_blob.lower() or "practical" in text_blob.lower()
