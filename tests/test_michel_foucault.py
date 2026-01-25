from socials_data import load_dataset
import pytest

def test_michel_foucault_dataset():
    ds = load_dataset("michel_foucault")
    assert len(ds) >= 1

    # Check for text presence
    all_text = " ".join([item["text"] for item in ds])
    assert "Panopticon" in all_text
    assert "bio-power" in all_text
