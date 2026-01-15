import pytest
from socials_data.core.loader import load_dataset
import os

def test_load_rene_descartes_dataset():
    """Test loading the René Descartes dataset."""
    dataset = load_dataset("rene_descartes")

    assert len(dataset) > 0
    assert "text" in dataset[0]

    # Check if the text content matches what we expect from Discourse on Method
    found_quote = False
    for entry in dataset:
        if "COGITO ERGO SUM" in entry["text"]:
            found_quote = True
            break

    assert found_quote, "The famous quote 'COGITO ERGO SUM' should be present in the dataset."

def test_rene_descartes_metadata():
    """Test that the metadata is correct."""
    import json
    metadata_path = "socials_data/personalities/rene_descartes/metadata.json"
    assert os.path.exists(metadata_path)

    with open(metadata_path, "r") as f:
        metadata = json.load(f)

    assert metadata["name"] == "René Descartes"
    assert metadata["id"] == "rene_descartes"
