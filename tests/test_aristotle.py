from socials_data import load_dataset
import pytest

def test_aristotle():
    ds = load_dataset("aristotle")
    assert len(ds) >= 1
    text = ds[0]["text"]
    assert "Every art and every inquiry" in text
    assert "Nicomachean Ethics" in ds[0]["source"] or "nicomachean_ethics" in ds[0]["source"]
