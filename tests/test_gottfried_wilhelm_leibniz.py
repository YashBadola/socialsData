import pytest
from socials_data.core.loader import load_dataset
from socials_data.core.manager import PersonalityManager

def test_leibniz_dataset_structure():
    # Test that the dataset can be loaded
    dataset = load_dataset('gottfried_wilhelm_leibniz')
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
        'monadology.txt'
    }
    assert sources == expected_sources

def test_leibniz_content():
    dataset = load_dataset('gottfried_wilhelm_leibniz')

    # Search for key Leibnizian terms to verify content
    text = dataset[0]['text']
    keywords = ["monad", "sufficient reason", "God", "simple substance", "preestablished harmony"]

    found_keywords = [kw for kw in keywords if kw.lower() in text.lower()]
    assert len(found_keywords) >= 3, f"Expected to find Leibnizian keywords, but found: {found_keywords}"

def test_leibniz_metadata():
    manager = PersonalityManager()
    metadata = manager.get_metadata('gottfried_wilhelm_leibniz')

    assert metadata['name'] == 'Gottfried Wilhelm Leibniz'
    assert 'system_prompt' in metadata
    assert 'best of all possible worlds' in metadata['system_prompt'].lower()
    assert len(metadata['sources']) == 1
