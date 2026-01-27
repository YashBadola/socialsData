import pytest
from socials_data.core.loader import load_dataset
from socials_data.core.manager import PersonalityManager

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
        'fear_and_trembling.txt',
        'sickness_unto_death.txt',
        'either_or.txt'
    }
    assert sources == expected_sources, f"Sources mismatch: {sources}"

def test_soren_kierkegaard_content():
    dataset = load_dataset('soren_kierkegaard')

    # Search for key Kierkegaardian terms to verify content
    text = " ".join(dataset[:]['text'])
    keywords = ["despair", "faith", "paradox", "individual", "anxiety", "leap"]

    found_keywords = [kw for kw in keywords if kw.lower() in text.lower()]
    assert len(found_keywords) >= 3, f"Expected to find Kierkegaardian keywords, but found: {found_keywords}"

def test_soren_kierkegaard_metadata():
    manager = PersonalityManager()
    metadata = manager.get_metadata('soren_kierkegaard')

    assert metadata['name'] == 'Soren Kierkegaard'
    assert 'system_prompt' in metadata
    assert 'existential' in metadata['system_prompt'].lower()
    assert len(metadata['sources']) == 4
