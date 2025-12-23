
import pytest
from socials_data.core.loader import load_dataset
from socials_data.core.manager import PersonalityManager

def test_plato_dataset_loading():
    """Test that the Plato dataset can be loaded."""
    # This should load the dataset from the local processed directory
    dataset = load_dataset("plato")

    # Check that it returns a Hugging Face Dataset
    assert hasattr(dataset, "column_names")
    assert "text" in dataset.column_names
    assert "source" in dataset.column_names

    # Check that it's not empty
    assert len(dataset) > 0

    # Check a sample
    sample = dataset[0]
    assert isinstance(sample["text"], str)
    assert len(sample["text"]) > 100
    assert sample["source"] in ["republic.txt", "symposium.txt"]

def test_plato_content():
    """Test that the content contains expected keywords."""
    dataset = load_dataset("plato")

    # Concatenate first few texts to search for keywords
    text_sample = " ".join(dataset[:10]["text"])

    keywords = ["Socrates", "Glaucon", "justice", "truth", "soul"]
    # At least some of these should be present
    found = any(keyword in text_sample for keyword in keywords)
    assert found, f"None of the keywords {keywords} found in the sample text."

def test_plato_metadata():
    """Test that metadata is correct."""
    manager = PersonalityManager()
    metadata = manager.get_metadata("plato")

    assert metadata["name"] == "Plato"
    assert metadata["id"] == "plato"
    assert "The Republic" in [s["title"] for s in metadata["sources"]]
