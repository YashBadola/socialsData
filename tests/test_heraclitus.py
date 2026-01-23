import pytest
from socials_data.core.loader import load_dataset

def test_load_heraclitus_dataset():
    dataset = load_dataset("heraclitus")
    assert len(dataset) > 0

    # Check if we have fragments about fire/flux
    texts = [row["text"] for row in dataset]
    assert any("fire" in text for text in texts)
    assert any("river" in text for text in texts)
