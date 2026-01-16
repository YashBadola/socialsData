import pytest
from socials_data.core.loader import load_dataset
import os

@pytest.fixture
def simone_de_beauvoir_dataset():
    """Loads the Simone de Beauvoir dataset."""
    return load_dataset("simone_de_beauvoir")

def test_dataset_loading(simone_de_beauvoir_dataset):
    """Test that the dataset loads correctly."""
    assert simone_de_beauvoir_dataset is not None
    assert len(simone_de_beauvoir_dataset) > 0

def test_dataset_structure(simone_de_beauvoir_dataset):
    """Test that the dataset has the correct columns."""
    sample = simone_de_beauvoir_dataset[0]
    assert "text" in sample
    assert isinstance(sample["text"], str)

def test_content_presence(simone_de_beauvoir_dataset):
    """Test that the dataset contains expected content from the raw files."""
    texts = [item["text"] for item in simone_de_beauvoir_dataset]
    combined_text = " ".join(texts)

    assert "The Second Sex" in combined_text or "One is not born" in combined_text
    assert "Ethics of Ambiguity" in combined_text or "continuously work" in combined_text
    assert "Letters to Sartre" in combined_text or "Café de Flore" in combined_text

def test_metadata_consistency():
    """Test that the metadata is consistent with the processed data."""
    # This is a bit indirect, but we can check if the personality ID maps to the directory
    assert os.path.exists("socials_data/personalities/simone_de_beauvoir/metadata.json")
    assert os.path.exists("socials_data/personalities/simone_de_beauvoir/processed/data.jsonl")
