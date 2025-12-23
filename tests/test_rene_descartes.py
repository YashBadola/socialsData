
import pytest
from socials_data import load_dataset
from socials_data.core.manager import PersonalityManager

def test_rene_descartes_exists():
    manager = PersonalityManager()
    personalities = manager.list_personalities()
    assert "rene_descartes" in personalities

def test_rene_descartes_metadata():
    manager = PersonalityManager()
    metadata = manager.get_metadata("rene_descartes")
    assert metadata["name"] == "Rene Descartes"
    assert metadata["id"] == "rene_descartes"
    assert len(metadata["sources"]) == 3

def test_load_dataset():
    dataset = load_dataset("rene_descartes")
    assert len(dataset) > 0
    # Check for some expected content
    found_method = False
    found_cogito = False

    # We are looking for key phrases in the text
    for item in dataset:
        text = item["text"]
        if "Discourse on the Method" in text or "method" in text.lower():
            found_method = True
        if "think" in text.lower() and "exist" in text.lower(): # Loose check for Cogito
            found_cogito = True

    assert found_method
    assert found_cogito
