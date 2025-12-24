import os
import pytest
from socials_data.core.loader import load_dataset
from socials_data.core.manager import PersonalityManager

@pytest.fixture
def personality_id():
    return "aristotle"

def test_personality_exists(personality_id):
    """Test that the personality exists in the manager."""
    manager = PersonalityManager()
    personalities = manager.list_personalities()
    assert personality_id in personalities

def test_metadata_structure(personality_id):
    """Test that the metadata contains required fields."""
    manager = PersonalityManager()
    metadata = manager.get_metadata(personality_id)

    assert metadata['name'] == "Aristotle"
    assert "system_prompt" in metadata
    assert "teleological" in metadata['system_prompt'].lower()
    assert "eudaimonia" in metadata['system_prompt'].lower()

    assert len(metadata['sources']) == 4
    titles = [s['title'] for s in metadata['sources']]
    assert "The Nicomachean Ethics" in titles
    assert "Politics" in titles
    assert "Poetics" in titles
    assert "History of Animals" in titles

def test_load_dataset(personality_id):
    """Test that the dataset loads correctly."""
    dataset = load_dataset(personality_id)
    assert len(dataset) > 0

    # Check a sample
    sample = dataset[0]
    assert "text" in sample
    assert "source" in sample
    assert isinstance(sample['text'], str)
    assert len(sample['text']) > 0

def test_content_relevance(personality_id):
    """Test that the content is actually from Aristotle's works."""
    dataset = load_dataset(personality_id)

    # We should find some key terms in the dataset
    text_content = " ".join([d['text'] for d in dataset])

    # Check for terms specific to each book
    assert "virtue" in text_content.lower() # Ethics
    assert "state" in text_content.lower() or "city" in text_content.lower() # Politics
    assert "tragedy" in text_content.lower() or "poetry" in text_content.lower() # Poetics
    assert "animals" in text_content.lower() or "parts" in text_content.lower() # History of Animals

def test_no_gutenberg_markers(personality_id):
    """Test that Gutenberg headers/footers are stripped."""
    dataset = load_dataset(personality_id)
    for item in dataset:
        text = item['text']
        assert "*** START OF THE PROJECT GUTENBERG EBOOK" not in text
        assert "*** END OF THE PROJECT GUTENBERG EBOOK" not in text
