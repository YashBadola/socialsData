from socials_data import load_dataset
import pytest

def test_machiavelli():
    ds = load_dataset("niccolo_machiavelli")
    assert len(ds) >= 1
    text = ds[0]["text"]
    assert "Nicolo Machiavelli" in text
    assert "The Prince" in text
