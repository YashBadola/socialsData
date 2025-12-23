import pytest
import os
import json
from socials_data.core.loader import load_dataset
from socials_data.core.manager import PersonalityManager

def test_load_dataset_david_hume():
    """Test loading the David Hume dataset."""
    dataset = load_dataset('david_hume')

    assert dataset is not None, "Dataset should not be None"
    assert len(dataset) > 0, "Dataset should not be empty"

    # Check the schema
    sample = dataset[0]
    assert 'text' in sample
    assert 'source' in sample

    # Check content relevance
    text_content = [item['text'] for item in dataset]
    # Hume keywords
    keywords = ['impression', 'idea', 'cause', 'effect', 'reason', 'passion', 'skepticism', 'experience']

    found_keywords = False
    for text in text_content:
        if any(keyword in text.lower() for keyword in keywords):
            found_keywords = True
            break

    assert found_keywords, "Dataset should contain Hume-related keywords"

def test_metadata_david_hume():
    """Test metadata for David Hume."""
    manager = PersonalityManager()
    metadata = manager.get_metadata('david_hume')

    assert metadata['name'] == 'David Hume'
    assert metadata['id'] == 'david_hume'
    assert 'empiricism' in metadata['description'].lower()
    assert 'skepticism' in metadata['system_prompt'].lower()
    assert len(metadata['sources']) >= 2
