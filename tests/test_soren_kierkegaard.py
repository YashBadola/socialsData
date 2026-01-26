from socials_data import load_dataset
import pytest

def test_soren_kierkegaard():
    ds = load_dataset("soren_kierkegaard")
    assert len(ds) > 0
    all_text = " ".join([item["text"] for item in ds])
    # Check for key concepts/names in the text
    assert "Abraham" in all_text
    assert "Isaac" in all_text
    assert "Regine" in all_text
