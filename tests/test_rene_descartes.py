from socials_data import load_dataset
import pytest

def test_load_rene_descartes():
    ds = load_dataset("rene_descartes")
    assert len(ds) > 0
    # Check if the first entry contains some text
    assert "text" in ds[0]
    assert len(ds[0]["text"]) > 100
    # Check if Discourse on Method is in the text
    assert "Discourse" in ds[0]["text"]
