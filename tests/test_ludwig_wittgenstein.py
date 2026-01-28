import pytest
from socials_data.core.loader import load_dataset
from socials_data.core.manager import PersonalityManager
import os
import json

def test_ludwig_wittgenstein_dataset_structure():
    # Test that the dataset can be loaded
    dataset = load_dataset('ludwig_wittgenstein')
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
        'tractatus.txt',
        'investigations.txt'
    }
    # Note: sources in the dataset are filenames
    assert expected_sources.issubset(sources) or sources.issubset(expected_sources), f"Sources mismatch: {sources}"

def test_ludwig_wittgenstein_content():
    dataset = load_dataset('ludwig_wittgenstein')

    # Search for key Wittgenstein terms to verify content
    text = " ".join(dataset['text'])
    keywords = ["world", "fact", "game", "language", "silent", "beetle"]

    found_keywords = [kw for kw in keywords if kw.lower() in text.lower()]
    assert len(found_keywords) > 0, f"Expected to find Wittgenstein keywords, but found: {found_keywords}"

def test_ludwig_wittgenstein_metadata():
    manager = PersonalityManager()
    metadata = manager.get_metadata('ludwig_wittgenstein')

    assert metadata['name'] == 'Ludwig Wittgenstein'
    assert 'system_prompt' in metadata
    assert 'Tractatus' in metadata['system_prompt']
    assert len(metadata['sources']) == 2
