import os
import pytest
from socials_data.core.loader import load_dataset
from socials_data.core.manager import PersonalityManager

@pytest.fixture
def manager():
    return PersonalityManager()

def test_rousseau_exists(manager):
    personalities = manager.list_personalities()
    assert "jean_jacques_rousseau" in personalities

def test_rousseau_metadata(manager):
    metadata = manager.get_metadata("jean_jacques_rousseau")
    assert metadata["name"] == "Jean-Jacques Rousseau"
    assert "Enlightenment" in metadata["description"]
    assert "General Will" in metadata["system_prompt"]
    assert len(metadata["sources"]) >= 3

def test_load_rousseau_dataset():
    dataset = load_dataset("jean_jacques_rousseau")
    assert dataset is not None
    # We expect some data
    assert len(dataset) > 0

    # Check sample content
    sample = dataset[0]
    assert "text" in sample
    assert "source" in sample

    # Check for keywords
    texts = [row["text"] for row in dataset]
    # We should find mentions of "social contract" or "inequality" or "Emile"
    # Since we have full texts, these words are guaranteed.
    combined = " ".join(texts[:100]) # Check first 100 chunks

    # Check for specific source files
    sources = set([row["source"] for row in dataset])
    assert "social_contract_and_discourses.txt" in sources
    assert "confessions.txt" in sources
    assert "emile.txt" in sources

    # Negative assertion: check for license text
    # We stripped "START OF THE PROJECT" and "END OF THE PROJECT"
    # So "Project Gutenberg License" should mostly be gone, unless it appears in the middle (unlikely).
    # "The Project Gutenberg eBook" usually appears in header/footer.

    for text in texts[:50]: # Check a sample
        assert "START OF THE PROJECT GUTENBERG" not in text
        assert "END OF THE PROJECT GUTENBERG" not in text
