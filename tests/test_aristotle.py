from socials_data import load_dataset
import pytest

def test_aristotle():
    ds = load_dataset("aristotle")
    assert len(ds) == 2
    all_text = " ".join([item["text"] for item in ds])
    # Check for presence of key terms
    assert "Ethics" in all_text
    assert "Politics" in all_text
