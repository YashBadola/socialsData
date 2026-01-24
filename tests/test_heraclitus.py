import pytest
from socials_data.core.loader import load_dataset

def test_load_heraclitus_dataset():
    """
    Test that the Heraclitus dataset can be loaded and contains expected text.
    """
    dataset = load_dataset("heraclitus")
    assert len(dataset) > 0, "Dataset should not be empty"

    # Check for a specific fragment to ensure content is correct
    texts = [item['text'] for item in dataset]
    found_fragment = any("You cannot step twice into the same rivers" in text for text in texts)
    assert found_fragment, "Could not find the famous river fragment in the dataset"

    # Check source
    sources = [item['source'] for item in dataset]
    assert "flux.txt" in sources
