from socials_data.core.loader import load_dataset
import pytest

def test_kierkegaard_dataset_loading():
    """Test if Kierkegaard dataset loads correctly."""
    dataset = load_dataset("soren_kierkegaard")

    # Check if dataset is not empty
    assert len(dataset) > 0

    # Check if we have the expected number of entries (we added 2 files)
    assert len(dataset) == 2

    # Check content of one of the entries
    texts = [item['text'] for item in dataset]
    assert any("What is a poet?" in text for text in texts)
    assert any("Faith is precisely this paradox" in text for text in texts)
