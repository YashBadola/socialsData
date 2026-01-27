from socials_data import load_dataset
import pytest

def test_diogenes_workflow():
    ds = load_dataset("diogenes_of_sinope")
    assert len(ds) > 0
    all_text = " ".join([item["text"] for item in ds])
    assert "Alexander" in all_text
    assert "lamp" in all_text
    assert "featherless biped" in all_text
