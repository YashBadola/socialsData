import os
import pytest
from socials_data.core.manager import PersonalityManager
from socials_data.core.loader import load_dataset as pkg_load_dataset

@pytest.fixture
def personality_id():
    return "aristotle"

def test_personality_exists(personality_id):
    manager = PersonalityManager()
    personalities = manager.list_personalities()
    assert personality_id in personalities

def test_metadata_structure(personality_id):
    manager = PersonalityManager()
    metadata = manager.get_metadata(personality_id)

    assert metadata["name"] == "Aristotle"
    assert metadata["id"] == personality_id
    assert "system_prompt" in metadata
    assert "sources" in metadata
    assert len(metadata["sources"]) == 4

    for source in metadata["sources"]:
        assert "title" in source
        assert "url" in source
        assert "type" in source
        assert "license" in source

def test_raw_files_exist(personality_id):
    # This test assumes the test is running in the repo root
    base_path = f"socials_data/personalities/{personality_id}/raw"
    expected_files = [
        "nicomachean_ethics.txt",
        "politics.txt",
        "poetics.txt",
        "categories.txt"
    ]

    for filename in expected_files:
        assert os.path.exists(os.path.join(base_path, filename))

def test_dataset_loading(personality_id):
    # We need to ensure we are loading the local dataset, not from HF Hub (though loader handles this)
    dataset = pkg_load_dataset(personality_id)
    assert dataset is not None
    assert len(dataset) > 0

    # Check schema
    sample = dataset[0]
    assert "text" in sample
    assert "source" in sample

    # Check content relevance
    # Since we have many chunks, we scan a few to find characteristic words
    found_keyword = False
    keywords = ["virtue", "state", "nature", "man", "happiness", "tragedy", "substance", "quality"]

    # Check first 20 samples
    for i in range(min(len(dataset), 20)):
        text = dataset[i]["text"].lower()
        if any(k in text for k in keywords):
            found_keyword = True
            break

    assert found_keyword, "Did not find expected keywords in the first 20 samples"
