from socials_data.core.loader import load_dataset
import pytest

def test_load_rene_descartes_dataset():
    """Test loading the René Descartes dataset."""
    dataset = load_dataset("rené_descartes")
    assert len(dataset) > 0
    assert "text" in dataset[0]
    assert "René Descartes" in dataset[0]["text"]

def test_rene_descartes_content():
    """Test the content of the René Descartes dataset."""
    dataset = load_dataset("rené_descartes")
    text = dataset[0]["text"]
    assert "COGITO ERGO SUM" in text
    assert "DISCOURSE ON THE METHOD" in text
