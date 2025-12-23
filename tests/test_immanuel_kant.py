import pytest
from socials_data.core.loader import load_dataset
from socials_data.core.manager import PersonalityManager
import os
import json

def test_immanuel_kant_dataset_structure():
    # Test that the dataset can be loaded
    dataset = load_dataset('immanuel_kant')
    assert len(dataset) > 0, "Dataset should not be empty"

    # Check sample structure
    sample = dataset[0]
    assert 'text' in sample
    assert 'source' in sample
    assert isinstance(sample['text'], str)
    assert isinstance(sample['source'], str)

    # Check that sources match expected files
    sources = set(dataset['source'])
    expected_sources = {
        'critique_of_pure_reason.txt',
        'critique_of_practical_reason.txt',
        'metaphysic_of_morals.txt',
        'perpetual_peace.txt'
    }
    # Note: sources in the dataset are filenames
    assert sources.issubset(expected_sources) or expected_sources.issubset(sources), f"Sources mismatch: {sources}"

def test_immanuel_kant_content():
    dataset = load_dataset('immanuel_kant')

    # Search for key Kantian terms to verify content
    text = " ".join(dataset[:100]['text'])
    keywords = ["reason", "moral", "law", "imperative", "pure", "practical"]

    found_keywords = [kw for kw in keywords if kw.lower() in text.lower()]
    assert len(found_keywords) > 0, f"Expected to find Kantian keywords, but found: {found_keywords}"

def test_immanuel_kant_metadata():
    manager = PersonalityManager()
    metadata = manager.get_metadata('immanuel_kant')

    assert metadata['name'] == 'Immanuel Kant'
    assert 'system_prompt' in metadata
    assert 'Categorical Imperative' in metadata['system_prompt']
    assert len(metadata['sources']) == 4
