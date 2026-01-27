from socials_data import load_dataset
import pytest

def test_michel_de_montaigne():
    ds = load_dataset("michel_de_montaigne")
    assert len(ds) >= 1
    # Check that at least one item contains "Essays" or "Montaigne"
    found = False
    for item in ds:
        if "Montaigne" in item["text"]:
            found = True
            break
    assert found
