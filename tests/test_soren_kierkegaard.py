from socials_data import load_dataset
import pytest

def test_soren_kierkegaard():
    ds = load_dataset("soren_kierkegaard")
    assert len(ds) >= 1
    all_text = " ".join([item["text"] for item in ds])
    assert "The crowd is untruth" in all_text
    assert "Anxiety is the dizziness of freedom" in all_text
