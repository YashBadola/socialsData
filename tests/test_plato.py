import pytest
from socials_data.core.loader import load_dataset

def test_load_plato_dataset():
    dataset = load_dataset('plato')
    assert len(dataset) > 0
    assert 'text' in dataset.features
    assert 'source' in dataset.features

def test_plato_content():
    dataset = load_dataset('plato')
    # Check that we have content from The Republic
    republic_content = any(entry['source'] == 'the_republic.txt' for entry in dataset)
    assert republic_content

    # Check that we have content from The Apology
    apology_content = any(entry['source'] == 'the_apology.txt' for entry in dataset)
    assert apology_content

    # Check that we have content from Symposium
    symposium_content = any(entry['source'] == 'symposium.txt' for entry in dataset)
    assert symposium_content

    # Check for keywords
    sample_text = " ".join([entry['text'] for entry in dataset])
    assert "Socrates" in sample_text
    assert "philosophy" in sample_text or "philosophical" in sample_text
