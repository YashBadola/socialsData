import os
import pytest
from socials_data import load_dataset
from socials_data.core.manager import PersonalityManager

def test_baruch_spinoza_dataset_loading():
    """
    Test that the Baruch Spinoza dataset can be loaded via the load_dataset API.
    """
    dataset = load_dataset("baruch_spinoza")

    # Check that it returns a Dataset object
    assert dataset is not None
    assert len(dataset) > 0

    # Check the first item
    first_item = dataset[0]
    assert "text" in first_item
    assert isinstance(first_item["text"], str)
    assert len(first_item["text"]) > 0

    # Check for keywords from "The Ethics"
    ethics_found = False
    ethics_keywords = ["self--caused", "substance", "attribute", "mode"]

    # Check for keywords from "Tractatus Theologico-Politicus"
    # Looking for terms like "prophecy", "Hebrew", "commonwealth", "divine law"
    tractatus_found = False
    tractatus_keywords = ["prophecy", "superstition", "commonwealth", "sovereign", "Hebrew"]

    # We iterate through enough samples to ensure we hit both books if they are chunked sequentially
    # Since we have two files, one might be processed before the other.

    for item in dataset:
        text = item["text"]
        if not ethics_found and any(k in text for k in ethics_keywords):
            ethics_found = True
        if not tractatus_found and any(k in text for k in tractatus_keywords):
            tractatus_found = True

        if ethics_found and tractatus_found:
            break

    assert ethics_found, "Did not find expected keywords from 'The Ethics'"
    assert tractatus_found, "Did not find expected keywords from 'Tractatus Theologico-Politicus'"

def test_baruch_spinoza_metadata():
    """
    Test that the metadata is correctly readable and contains expected fields.
    """
    manager = PersonalityManager()
    metadata = manager.get_metadata("baruch_spinoza")

    assert metadata["name"] == "Baruch Spinoza"
    assert metadata["id"] == "baruch_spinoza"
    assert "Rationalist" in metadata["system_prompt"]
    assert len(metadata["sources"]) == 2
    assert metadata["sources"][0]["title"] == "The Ethics"
    assert metadata["sources"][1]["title"] == "Tractatus Theologico-Politicus"

if __name__ == "__main__":
    pytest.main([__file__])
