import pytest
from socials_data.core.manager import PersonalityManager
from socials_data import load_dataset as load_socials_dataset

def test_baruch_spinoza_metadata():
    manager = PersonalityManager()
    metadata = manager.get_metadata("baruch_spinoza")

    assert metadata["name"] == "Baruch Spinoza"
    assert metadata["id"] == "baruch_spinoza"
    assert len(metadata["sources"]) >= 3
    assert "Ethics" in metadata["sources"][0]["title"]

def test_baruch_spinoza_dataset_loading():
    # Load the dataset
    dataset = load_socials_dataset("baruch_spinoza")

    # Check it's not empty
    assert len(dataset) > 0

    # Check structure
    assert "text" in dataset.features
    assert "source" in dataset.features

    # Check content sample
    # Search for a keyword likely to be in Spinoza's work
    found_god_or_nature = False
    found_substance = False

    for item in dataset:
        text = item["text"].lower()
        if "nature" in text or "god" in text:
            found_god_or_nature = True
        if "substance" in text or "axiom" in text:
            found_substance = True

        if found_god_or_nature and found_substance:
            break

    assert found_god_or_nature, "Did not find 'God' or 'Nature' in text samples"
    assert found_substance, "Did not find 'substance' or 'axiom' in text samples"
