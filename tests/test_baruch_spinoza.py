import pytest
from socials_data.core.loader import load_dataset
from socials_data.core.manager import PersonalityManager
from pathlib import Path

def test_load_dataset():
    dataset = load_dataset("baruch_spinoza")
    assert len(dataset) > 0
    assert "text" in dataset[0]
    assert "source" in dataset[0]

    # Check for content specific to Spinoza
    found_keyword = False
    for i in range(min(len(dataset), 20)):
        if "God" in dataset[i]["text"] or "Nature" in dataset[i]["text"] or "substance" in dataset[i]["text"]:
            found_keyword = True
            break
    assert found_keyword, "Did not find expected keywords in the first 20 chunks"

def test_metadata():
    manager = PersonalityManager()
    metadata = manager.get_metadata("baruch_spinoza")
    assert metadata["name"] == "Baruch Spinoza"
    assert metadata["id"] == "baruch_spinoza"
    assert metadata["sources"][0]["title"] == "Ethics"
