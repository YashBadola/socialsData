import pytest
from socials_data import load_dataset
import os

def test_simone_de_beauvoir_structure():
    base_path = "socials_data/personalities/simone_de_beauvoir"
    assert os.path.exists(base_path)
    assert os.path.exists(os.path.join(base_path, "metadata.json"))
    assert os.path.exists(os.path.join(base_path, "raw"))
    assert os.path.exists(os.path.join(base_path, "processed"))
    assert os.path.exists(os.path.join(base_path, "processed", "data.jsonl"))

def test_simone_de_beauvoir_content():
    ds = load_dataset("simone_de_beauvoir")
    # We added 3 files, so there should be 3 items
    assert len(ds) == 3

    all_text = " ".join([item["text"] for item in ds])
    assert "One is not born, but rather becomes, a woman" in all_text
    assert "The man who finds himself cast into the world" in all_text
    assert "I was born at four o'clock in the morning" in all_text
