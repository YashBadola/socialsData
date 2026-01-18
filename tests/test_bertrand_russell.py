from socials_data import load_dataset
import pytest

def test_bertrand_russell():
    ds = load_dataset("bertrand_russell")
    assert len(ds) == 2
    all_text = " ".join([item["text"] for item in ds])
    # Check for content from the files
    # The titles in the text are uppercase
    assert "THE PROBLEMS OF PHILOSOPHY" in all_text
    assert "THE ANALYSIS OF MIND" in all_text
    assert "Bertrand Russell" in all_text
