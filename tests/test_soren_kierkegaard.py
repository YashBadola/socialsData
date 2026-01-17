import pytest
from socials_data import load_dataset
import os

def test_soren_kierkegaard_structure():
    base_path = "socials_data/personalities/soren_kierkegaard"
    assert os.path.exists(os.path.join(base_path, "metadata.json"))
    assert os.path.exists(os.path.join(base_path, "raw"))
    assert os.path.exists(os.path.join(base_path, "processed"))
    assert os.path.exists(os.path.join(base_path, "processed", "data.jsonl"))

def test_soren_kierkegaard_load():
    ds = load_dataset("soren_kierkegaard")
    assert len(ds) > 0
    assert "text" in ds[0]
    assert "source" in ds[0]
