from socials_data.core.loader import load_dataset
import pytest

def test_load_soren_kierkegaard_dataset():
    dataset = load_dataset("soren_kierkegaard")

    # Verify dataset structure
    assert dataset is not None
    assert len(dataset) > 0

    # Check first entry
    first_entry = dataset[0]
    assert 'text' in first_entry
    assert 'source' in first_entry

    # Verify content presence (checking part of the text we added)
    assert "Subjectivity is truth" in first_entry['text']
