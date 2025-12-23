import os
import pytest
from socials_data.core.loader import load_dataset

def test_david_hume_dataset():
    """Test that the David Hume dataset loads correctly and contains valid data."""
    dataset = load_dataset('david_hume')

    # Check that it returns a Dataset object
    assert hasattr(dataset, 'features')
    assert len(dataset) > 0

    # Check a sample
    sample = dataset[0]
    assert 'text' in sample
    assert 'source' in sample

    # Verify content
    text_content = sample['text']
    assert isinstance(text_content, str)
    assert len(text_content) > 0

    # Check for expected terms (sanity check)
    # Since we cleaned the text, we might not find "Project Gutenberg"
    # But we should find "Hume", "idea", "impression", "reason", etc.
    # Note: dataset is chunked, so we check if *any* chunk has these words, or just check general validity.

    # Let's check that sources are correct
    sources = set(dataset['source'])
    assert 'enquiry.txt' in sources
    assert 'treatise.txt' in sources

if __name__ == "__main__":
    test_david_hume_dataset()
