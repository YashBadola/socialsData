from socials_data import load_dataset
import pytest

def test_vitruvius_data():
    ds = load_dataset("vitruvius")
    assert len(ds) >= 1
    text = ds[0]["text"]
    # Check for Vitruvius (case insensitive just in case, but usually it preserves case)
    assert "VITRUVIUS" in text or "Vitruvius" in text
    # Check for title
    assert "THE TEN BOOKS ON ARCHITECTURE" in text or "The Ten Books on Architecture" in text
