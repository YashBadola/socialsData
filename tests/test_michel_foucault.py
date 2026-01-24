from socials_data import load_dataset
import pytest

def test_michel_foucault():
    ds = load_dataset("michel_foucault")
    # We put everything in one file, so it might be 1 entry or split by newlines depending on implementation.
    # The read_file output showed "text": "The gesture... \n Is it surprising... " all in one string.
    # So len(ds) should be 1.
    assert len(ds) == 1
    all_text = ds[0]["text"]
    assert "The gesture that divides madness" in all_text
    assert "Is it surprising that prisons resemble factories" in all_text
    assert "Power is everywhere" in all_text

if __name__ == "__main__":
    test_michel_foucault()
