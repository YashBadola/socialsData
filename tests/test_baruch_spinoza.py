import pytest
from socials_data import load_dataset
from socials_data.core.manager import PersonalityManager

def test_baruch_spinoza_dataset_loading():
    """Test that the Baruch Spinoza dataset loads correctly."""
    dataset = load_dataset("baruch_spinoza")

    assert dataset is not None
    assert len(dataset) > 0

    # Check that the text contains expected keywords
    # Spinoza uses words like "Substance", "God", "Attribute", "Mode", "Nature"

    # Since dataset slicing returns a dict of lists, we grab the 'text' list
    sample_texts = dataset[:10]["text"]

    found_keyword = False
    keywords = ["God", "Nature", "Substance", "Attribute", "Mode", "Ethics"]

    for text in sample_texts:
        for keyword in keywords:
            if keyword in text:
                found_keyword = True
                break
        if found_keyword:
            break

    assert found_keyword, "Could not find expected keywords in the first 10 samples."

def test_baruch_spinoza_metadata():
    """Test that the Baruch Spinoza metadata is correct."""
    manager = PersonalityManager()
    metadata = manager.get_metadata("baruch_spinoza")

    assert metadata["name"] == "Baruch Spinoza"
    assert "Ethics" in metadata["sources"][0]["title"]
    assert metadata["id"] == "baruch_spinoza"
