import pytest
from socials_data import load_dataset
from socials_data.core.manager import PersonalityManager
import os

def test_voltaire_dataset_structure():
    """Test that the Voltaire dataset loads correctly and has the expected structure."""
    dataset = load_dataset("voltaire")

    assert dataset is not None
    assert len(dataset) > 0
    assert "text" in dataset.features

    # Check that at least one entry comes from each source file
    texts = [item['text'] for item in dataset]
    sources = [item['source'] for item in dataset]

    assert any("candide_excerpt.txt" in s for s in sources)
    assert any("philosophical_dictionary.txt" in s for s in sources)
    assert any("letters_on_england.txt" in s for s in sources)

def test_voltaire_metadata():
    """Test that the Voltaire metadata is correct."""
    manager = PersonalityManager()

    metadata = manager.get_metadata("voltaire")

    assert metadata['name'] == "Voltaire"
    assert metadata['id'] == "voltaire"
    assert len(metadata['sources']) == 3

def test_voltaire_content_check():
    """Test specific content presence."""
    dataset = load_dataset("voltaire")

    found_candide = False
    found_liberty = False

    for item in dataset:
        if "Westphalia" in item['text']:
            found_candide = True
        if "What is liberty?" in item['text']:
            found_liberty = True

    assert found_candide
    assert found_liberty
