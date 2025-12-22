import pytest
from socials_data.core.manager import PersonalityManager
from socials_data import load_dataset

def test_baruch_spinoza_dataset_loading():
    """Test that the Baruch Spinoza dataset loads correctly."""
    dataset = load_dataset("baruch_spinoza")

    assert dataset is not None
    assert len(dataset) > 0

    # Check schema
    assert "text" in dataset.column_names
    assert "source" in dataset.column_names

    # Check content for specific keywords
    # Since dataset is a Hugging Face dataset, we can iterate or sample
    sample_text = dataset[0]["text"]
    assert isinstance(sample_text, str)
    assert len(sample_text) > 0

    # We can check for some Spinoza keywords in the entire dataset or a sample
    keywords = ["God", "Nature", "substance", "attribute", "mode", "affect", "mind", "body"]
    found_keywords = False

    # Check first few entries
    for i in range(min(5, len(dataset))):
        text = dataset[i]["text"]
        if any(k in text for k in keywords):
            found_keywords = True
            break

    assert found_keywords, "Spinoza keywords not found in the first few samples"

def test_baruch_spinoza_metadata():
    """Test that metadata for Baruch Spinoza is correct."""
    manager = PersonalityManager()
    metadata = manager.get_metadata("baruch_spinoza")

    assert metadata["name"] == "Baruch Spinoza"
    assert "Rationalism" in metadata["description"]
    assert "God and Nature" in metadata["system_prompt"]
