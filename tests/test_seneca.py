from socials_data import load_dataset
import pytest

def test_seneca():
    ds = load_dataset("seneca")
    assert len(ds) > 0
    all_text = " ".join([item["text"] for item in ds])
    assert "Seneca" in all_text or "SENECA" in all_text
    assert "BENEFITS" in all_text or "benefits" in all_text
    assert "Happy Life" in all_text or "HAPPY LIFE" in all_text
