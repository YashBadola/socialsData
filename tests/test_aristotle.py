from socials_data import load_dataset
import pytest

def test_aristotle():
    ds = load_dataset("aristotle")
    assert len(ds) == 2
    all_text = " ".join([item["text"] for item in ds])
    assert "political animal" in all_text
    assert "Nicomachean Ethics" in all_text or "Every art and every inquiry" in all_text
