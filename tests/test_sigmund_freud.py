import os
import pytest
from socials_data import load_dataset
from socials_data.core.manager import PersonalityManager

def test_sigmund_freud_dataset():
    # Load dataset
    dataset = load_dataset('sigmund_freud')

    # Check if dataset is not empty
    assert len(dataset) > 0, "Dataset is empty"

    # Check if samples have expected fields
    sample = dataset[0]
    assert 'text' in sample
    assert 'source' in sample

    # Check if source filenames are correct
    sources = set(dataset['source'])
    expected_sources = {
        'the_interpretation_of_dreams.txt',
        'dream_psychology.txt',
        'totem_and_taboo.txt',
        'psychopathology_of_everyday_life.txt',
        'a_general_introduction_to_psychoanalysis.txt'
    }

    # It's possible not all sources are in the first chunk if dataset is huge,
    # but load_dataset should load all.
    # The processed data is in chunks.

    # Let's verify at least one of them is present in the source column
    assert any(s in sources for s in expected_sources)

    # Check for keywords in text
    keywords = ['dream', 'unconscious', 'psychoanalysis', 'neurosis', 'ego']
    found_keywords = False
    for item in dataset:
        text = item['text'].lower()
        if any(k in text for k in keywords):
            found_keywords = True
            break

    assert found_keywords, "No relevant keywords found in the dataset"

    # Check for absence of Gutenberg headers (negative assertion)
    gutenberg_markers = [
        "Project Gutenberg",
        "START OF THE PROJECT GUTENBERG",
        "END OF THE PROJECT GUTENBERG"
    ]

    # Scan a subset of the dataset to save time, or all if small enough
    for item in dataset:
        text = item['text']
        for marker in gutenberg_markers:
            assert marker not in text, f"Found Gutenberg marker in text: {marker}"

    # Check metadata
    manager = PersonalityManager()
    metadata = manager.get_metadata('sigmund_freud')
    assert metadata['name'] == 'Sigmund Freud'
    assert len(metadata['sources']) == 5

if __name__ == "__main__":
    test_sigmund_freud_dataset()
