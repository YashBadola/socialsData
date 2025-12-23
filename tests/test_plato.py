import json
import pytest
from pathlib import Path
from socials_data.core.manager import PersonalityManager
from socials_data import load_dataset as pkg_load_dataset

@pytest.fixture
def personality_id():
    return "plato"

@pytest.fixture
def manager():
    return PersonalityManager()

def test_personality_exists(manager, personality_id):
    personalities = manager.list_personalities()
    assert personality_id in personalities

def test_metadata_structure(manager, personality_id):
    metadata = manager.get_metadata(personality_id)
    assert metadata["id"] == personality_id
    assert "name" in metadata
    assert "description" in metadata
    assert "system_prompt" in metadata
    assert "sources" in metadata
    assert isinstance(metadata["sources"], list)
    assert len(metadata["sources"]) == 3
    assert metadata["sources"][0]["title"] == "The Republic"

def test_raw_files_exist(personality_id):
    base_path = Path("socials_data/personalities") / personality_id / "raw"
    expected_files = ["the_republic.txt", "apology.txt", "symposium.txt"]
    for filename in expected_files:
        assert (base_path / filename).exists()

def test_processed_files_exist(personality_id):
    base_path = Path("socials_data/personalities") / personality_id / "processed"
    assert (base_path / "data.jsonl").exists()

def test_load_dataset_function(personality_id):
    # This tests the exported load_dataset function
    dataset = pkg_load_dataset(personality_id)
    assert len(dataset) > 0

    # Check sample structure
    sample = dataset[0]
    assert "text" in sample
    assert "source" in sample
    assert isinstance(sample["text"], str)
    assert isinstance(sample["source"], str)

    # Check that we have data from different sources
    sources = set(dataset["source"])
    assert "the_republic.txt" in sources
    # It's possible Apology or Symposium are small and might be chunked differently or lumped,
    # but they are big enough to be there.
    assert "apology.txt" in sources
    assert "symposium.txt" in sources

def test_content_relevance(personality_id):
    dataset = pkg_load_dataset(personality_id)
    # Search for keywords that should definitely be there
    text_content = " ".join(dataset["text"][:100]) # Check first 100 chunks

    keywords = ["Socrates", "justice", "soul", "virtue"]
    found = {k: False for k in keywords}

    for chunk in dataset["text"]:
        for k in keywords:
            if k in chunk:
                found[k] = True

    assert all(found.values()), f"Missing keywords: {[k for k, v in found.items() if not v]}"
