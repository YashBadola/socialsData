from socials_data import load_dataset
import pytest

def test_soren_kierkegaard():
    ds = load_dataset("soren_kierkegaard")
    assert len(ds) >= 1
    all_text = " ".join([item["text"] for item in ds])
    assert "Either/Or" in all_text or "Preface" in all_text
    assert "The Unhappiest Man" in all_text
