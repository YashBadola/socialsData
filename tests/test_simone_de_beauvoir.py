import pytest
from socials_data import load_dataset
import os

def test_simone_de_beauvoir_structure():
    base_path = "socials_data/personalities/simone_de_beauvoir"
    assert os.path.exists(os.path.join(base_path, "metadata.json"))
    assert os.path.exists(os.path.join(base_path, "raw"))
    assert os.path.exists(os.path.join(base_path, "processed"))
    assert os.path.exists(os.path.join(base_path, "processed", "data.jsonl"))

def test_simone_de_beauvoir_content():
    ds = load_dataset("simone_de_beauvoir")
    # We added 3 files
    assert len(ds) == 3

    all_text = " ".join([item["text"] for item in ds])

    # Check for key phrases from the added texts
    assert "One is not born, but rather becomes, a woman" in all_text
    assert "The word \"ambiguity\" is not a new one in philosophy" in all_text
    assert "I was born at four o'clock in the morning on the 9th of January 1908" in all_text

if __name__ == "__main__":
    test_simone_de_beauvoir_structure()
    test_simone_de_beauvoir_content()
