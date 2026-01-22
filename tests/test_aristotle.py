from socials_data import load_dataset
import pytest

def test_aristotle():
    ds = load_dataset("aristotle")
    # We expect 2 items: Nicomachean Ethics and Politics
    assert len(ds) == 2
    all_text = " ".join([item["text"] for item in ds])
    # Check for keywords from the texts
    assert "Nicomachean Ethics" in all_text
    assert "Politics" in all_text
    assert "Aristotle" in all_text
