import os
import pytest
from socials_data import load_dataset

def test_load_plato_dataset():
    dataset = load_dataset('plato')
    assert dataset is not None
    assert len(dataset) > 0

    # Check sample
    sample = dataset[0]
    assert 'text' in sample
    assert 'source' in sample
    assert isinstance(sample['text'], str)
    assert len(sample['text']) > 0

    # Check that we have content from both books (by checking sources generally)
    sources = set(item['source'] for item in dataset)
    assert 'the_republic.txt' in sources
    assert 'symposium.txt' in sources

    # Check for some keywords
    # dataset[:100] returns a dict of lists, so we just join the text column directly
    all_text = " ".join(dataset[:100]['text'])
    assert "Socrates" in all_text or "SOCRATES" in all_text
