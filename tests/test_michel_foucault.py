from socials_data import load_dataset
import pytest

def test_michel_foucault():
    ds = load_dataset("michel_foucault")
    assert len(ds) >= 1
    all_text = " ".join([item["text"] for item in ds])
    assert "Panopticon" in all_text
    assert "Biopower" in all_text
    assert "Repressive Hypothesis" in all_text

if __name__ == "__main__":
    test_michel_foucault()
