from socials_data import load_dataset
import pytest

def test_michel_foucault():
    ds = load_dataset("michel_foucault")
    assert len(ds) >= 1
    all_text = " ".join([item["text"] for item in ds])
    assert "History of Madness" in all_text
    assert "Panopticon" in all_text
    assert "biopower" in all_text
