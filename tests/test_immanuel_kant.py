import pytest
from socials_data import load_dataset

def test_immanuel_kant_dataset():
    dataset = load_dataset('immanuel_kant')
    assert dataset is not None
    assert len(dataset) > 0

    # Check first few entries for expected content
    sample = dataset[0]
    assert 'text' in sample
    assert isinstance(sample['text'], str)

    # Check for keywords that should appear in Kant's text
    text_content = " ".join([d['text'] for d in dataset])
    assert "reason" in text_content.lower()
    assert "pure" in text_content.lower()
    assert "critique" in text_content.lower() or "metaphysic" in text_content.lower()
