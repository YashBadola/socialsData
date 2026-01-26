import pytest
from socials_data.core.loader import load_dataset
from socials_data.core.manager import PersonalityManager
import os
import json

def test_soren_kierkegaard_dataset_structure():
    # Test that the dataset can be loaded
    dataset = load_dataset('soren_kierkegaard')
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
        'diapsalmata.txt',
        'in_vino_veritas.txt',
        'fear_and_trembling.txt'
    }
    # Note: sources in the dataset are filenames
    assert sources.issubset(expected_sources) or expected_sources.issubset(sources), f"Sources mismatch: {sources}"

def test_soren_kierkegaard_content():
    dataset = load_dataset('soren_kierkegaard')

    # Search for key Kierkegaardian terms to verify content
    text = " ".join(dataset[:100]['text'])
    # Using lowercase for case-insensitive search
    keywords = ["melancholy", "poet", "abraham", "faith", "love", "seduce", "fashion", "infinite"]

    found_keywords = [kw for kw in keywords if kw.lower() in text.lower()]
    assert len(found_keywords) > 0, f"Expected to find Kierkegaardian keywords, but found: {found_keywords}"

def test_soren_kierkegaard_metadata():
    manager = PersonalityManager()
    metadata = manager.get_metadata('soren_kierkegaard')

    assert metadata['name'] == 'Søren Kierkegaard'
    assert 'system_prompt' in metadata
    assert 'existentialist' in metadata['description'].lower()
    assert len(metadata['sources']) == 3
