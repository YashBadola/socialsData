import pytest
from socials_data.core.loader import load_dataset
from socials_data.core.manager import PersonalityManager

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
    assert sample['source'] == 'existentialism_is_a_humanism.txt'

def test_jean_paul_sartre_content():
    dataset = load_dataset('jean_paul_sartre')

    # Search for key terms to verify content
    text = " ".join([d['text'] for d in dataset])
    keywords = ["existentialism", "humanism", "choice", "responsibility", "freedom", "condemned"]

    found_keywords = [kw for kw in keywords if kw.lower() in text.lower()]
    # We expect all or most keywords to be present
    assert len(found_keywords) >= 4, f"Expected to find most keywords, but found: {found_keywords}"

    # Check for a specific quote or phrase
    assert "existence precedes essence" in text.lower()
    assert "condemned to be free" in text.lower()

def test_jean_paul_sartre_metadata():
    manager = PersonalityManager()
    metadata = manager.get_metadata('jean_paul_sartre')

    assert metadata['name'] == 'Jean-Paul Sartre'
    assert 'system_prompt' in metadata
    assert 'existence precedes essence' in metadata['system_prompt']
    assert len(metadata['sources']) == 1
    assert metadata['sources'][0]['title'] == 'Existentialism is a Humanism'
