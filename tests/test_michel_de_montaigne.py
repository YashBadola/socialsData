from socials_data import load_dataset
import pytest

def test_montaigne():
    ds = load_dataset("michel_de_montaigne")
    assert len(ds) > 0
    # Check for a known phrase
    all_text = " ".join([item["text"] for item in ds])
    assert "CHAPTER" in all_text
    print(f"Montaigne test passed with {len(ds)} items!")
