import pytest
from socials_data.core.loader import load_dataset
import os

def test_load_rene_descartes_dataset():
    """Test loading the Rene Descartes dataset."""
    dataset = load_dataset("rene_descartes")

    assert dataset is not None
    assert len(dataset) > 0
    assert "text" in dataset[0]
    assert "source" in dataset[0]

    # Check if the content matches what we expect
    first_text = dataset[0]["text"]
    assert "Good sense is, of all things among men, the most equally distributed" in first_text

def test_rene_descartes_files_exist():
    """Test that the files for Rene Descartes exist."""
    base_path = "socials_data/personalities/rene_descartes"
    assert os.path.exists(os.path.join(base_path, "metadata.json"))
    assert os.path.exists(os.path.join(base_path, "raw", "discourse_on_method.txt"))
    assert os.path.exists(os.path.join(base_path, "processed", "data.jsonl"))
