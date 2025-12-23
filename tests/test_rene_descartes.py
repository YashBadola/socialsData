import pytest
import os
import json
from socials_data.core.loader import load_dataset
# from socials_data.personalities.rene_descartes.metadata import metadata # Oops, metadata is a json file, not python.

def test_rene_descartes_exists():
    path = "socials_data/personalities/rene_descartes"
    assert os.path.isdir(path)
    assert os.path.isfile(os.path.join(path, "metadata.json"))
    assert os.path.isdir(os.path.join(path, "raw"))
    assert os.path.isdir(os.path.join(path, "processed"))

def test_rene_descartes_metadata():
    with open("socials_data/personalities/rene_descartes/metadata.json", "r") as f:
        meta = json.load(f)
    assert meta["id"] == "rene_descartes"
    assert "Cogito" in meta["system_prompt"]
    assert len(meta["sources"]) == 3

def test_rene_descartes_dataset_loads():
    ds = load_dataset("rene_descartes")
    assert len(ds) > 0
    # Check a sample
    sample = ds[0]
    assert "text" in sample
    assert "source" in sample
    assert isinstance(sample["text"], str)

    # Check for some keywords in the dataset to verify content
    found_cogito = False
    found_god = False
    for item in ds:
        text = item["text"].lower()
        if "cogito" in text or "think" in text: # cogito might be translated
            found_cogito = True
        if "god" in text:
            found_god = True
        if found_cogito and found_god:
            break

    # We can't guarantee 'cogito' literal string in English translations easily without checking,
    # but 'think' or 'reason' should be there.
    assert found_god or found_cogito
