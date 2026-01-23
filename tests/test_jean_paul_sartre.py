import pytest
from socials_data.core.loader import load_dataset
from socials_data.core.manager import PersonalityManager
import os
import json

def test_jean_paul_sartre_dataset_structure():
    # Test that the dataset can be loaded
    dataset = load_dataset('jean_paul_sartre')
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
        'existence_precedes_essence.txt',
        'bad_faith.txt',
        'freedom_and_responsibility.txt'
    }
    assert sources == expected_sources, f"Sources mismatch: {sources}"

def test_jean_paul_sartre_content():
    dataset = load_dataset('jean_paul_sartre')

    # Search for key Sartre terms to verify content
    text = " ".join(dataset[:100]['text'])
    keywords = ["existence", "essence", "freedom", "condemned", "bad faith"]

    found_keywords = [kw for kw in keywords if kw.lower() in text.lower()]
    assert len(found_keywords) > 0, f"Expected to find Sartre keywords, but found: {found_keywords}"

def test_jean_paul_sartre_metadata():
    manager = PersonalityManager()
    metadata = manager.get_metadata('jean_paul_sartre')

    assert metadata['name'] == 'Jean-Paul Sartre'
    assert 'system_prompt' in metadata
    assert 'for-itself' in metadata['system_prompt']
    assert len(metadata['sources']) == 3
