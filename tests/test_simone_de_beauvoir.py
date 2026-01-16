import pytest
from socials_data.core.loader import load_dataset
import os

@pytest.fixture
def simone_de_beauvoir_dataset():
    """Fixture to load the Simone de Beauvoir dataset."""
    return load_dataset("simone_de_beauvoir")

def test_simone_de_beauvoir_dataset_loading(simone_de_beauvoir_dataset):
    """Test if the dataset loads correctly."""
    assert simone_de_beauvoir_dataset is not None
    assert len(simone_de_beauvoir_dataset) > 0

def test_simone_de_beauvoir_dataset_structure(simone_de_beauvoir_dataset):
    """Test the structure of the dataset entries."""
    for entry in simone_de_beauvoir_dataset:
        assert "text" in entry
        assert isinstance(entry["text"], str)
        assert len(entry["text"]) > 0
        assert "source" in entry
        assert isinstance(entry["source"], str)

def test_simone_de_beauvoir_content(simone_de_beauvoir_dataset):
    """Test specific content presence in the dataset."""
    texts = [entry["text"] for entry in simone_de_beauvoir_dataset]
    combined_text = " ".join(texts)

    assert "One is not born, but rather becomes, a woman" in combined_text
    assert "The fundamental ambiguity of the human condition" in combined_text
    assert "MEMOIRS OF A DUTIFUL DAUGHTER" in combined_text
