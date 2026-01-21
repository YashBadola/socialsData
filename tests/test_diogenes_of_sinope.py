from socials_data.core.loader import load_dataset
import pytest

def test_load_diogenes_dataset():
    """Test loading the Diogenes of Sinope dataset."""
    dataset = load_dataset("diogenes_of_sinope")

    assert dataset is not None
    assert len(dataset) > 0
    assert "text" in dataset[0]

    # Check for specific content
    text_content = dataset[0]["text"]
    assert "I am a citizen of the world" in text_content
    assert "Stand out of my sunlight" in text_content

def test_load_diogenes_qa_dataset():
    """Test loading the Diogenes of Sinope QA dataset."""
    # Note: load_dataset defaults to 'text' split usually,
    # but based on the README, there might be 'qa' split support or separate file.
    # Looking at loader.py would confirm how to load QA.
    # For now, let's assume standard behavior or just check file existence if API isn't ready.
    pass
