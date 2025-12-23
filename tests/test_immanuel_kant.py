import json
import pytest
from socials_data.core.manager import PersonalityManager
from socials_data import load_dataset

@pytest.fixture
def personality_manager():
    return PersonalityManager()

def test_immanuel_kant_metadata(personality_manager):
    metadata = personality_manager.get_metadata("immanuel_kant")
    assert metadata["name"] == "Immanuel Kant"
    assert metadata["id"] == "immanuel_kant"
    assert len(metadata["sources"]) >= 2
    assert "The Critique of Pure Reason" in [s["title"] for s in metadata["sources"]]

def test_immanuel_kant_dataset_loading():
    dataset = load_dataset("immanuel_kant")
    assert len(dataset) > 0

    # Check first few entries
    sample = dataset[:5]
    assert "text" in sample
    assert "source" in sample

    # Verify content
    text_content = " ".join(sample["text"])
    assert "reason" in text_content.lower() or "critique" in text_content.lower()

    # Verify sources
    sources = set(sample["source"])
    assert "critique_of_pure_reason.txt" in sources or "critique_of_practical_reason.txt" in sources
