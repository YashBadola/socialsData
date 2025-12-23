
import pytest
from socials_data.core.manager import PersonalityManager
from socials_data.core.loader import load_dataset as loader_load_dataset

def test_aristotle_exists():
    manager = PersonalityManager()
    metadata = manager.get_metadata('aristotle')
    assert metadata['name'] == 'Aristotle'
    assert metadata['id'] == 'aristotle'
    assert len(metadata['sources']) == 3

def test_aristotle_dataset_loading():
    # Test loading the dataset
    # We use a mocked path or just assume the file is there since we created it
    dataset = loader_load_dataset('aristotle')
    assert len(dataset) > 0

    # Check first item structure
    item = dataset[0]
    assert 'text' in item
    assert 'source' in item
    assert isinstance(item['text'], str)
    assert len(item['text']) > 0

    # Verify content from one of the books is present
    # Check for "virtue" or "ethics" or "state" which are common
    found_keyword = False
    for i in range(min(len(dataset), 100)):
        text = dataset[i]['text'].lower()
        if 'virtue' in text or 'state' in text or 'tragedy' in text or 'nature' in text:
            found_keyword = True
            break

    assert found_keyword, "Did not find expected keywords in the first 100 chunks"

def test_aristotle_sources_in_dataset():
    dataset = loader_load_dataset('aristotle')
    sources = set(dataset['source'])
    expected_sources = {'nicomachean_ethics.txt', 'politics.txt', 'poetics.txt'}

    # Check if at least some of the sources are present
    assert sources.intersection(expected_sources)
