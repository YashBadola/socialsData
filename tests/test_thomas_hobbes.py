import os
import pytest
from socials_data.core.loader import load_dataset
from socials_data.core.manager import PersonalityManager

def test_thomas_hobbes_exists():
    manager = PersonalityManager()
    personalities = manager.list_personalities()
    assert 'thomas_hobbes' in personalities

def test_load_dataset():
    # Load the dataset
    dataset = load_dataset('thomas_hobbes')

    # Check it's not empty
    assert len(dataset) > 0

    # Check the content of the first item
    first_item = dataset[0]
    assert 'text' in first_item
    assert 'source' in first_item

    text = first_item['text']
    assert len(text) > 1000  # Should be substantial text

    # Check for keywords specific to Leviathan
    assert "Commonwealth" in text or "Common-wealth" in text
    assert "Soveraignty" in text or "Sovereignty" in text
    assert "brutish" in text or "nasty" in text
    assert "Leviathan" in text

def test_source_correctness():
    dataset = load_dataset('thomas_hobbes')
    unique_sources = set(item['source'] for item in dataset)
    assert 'leviathan.txt' in unique_sources
