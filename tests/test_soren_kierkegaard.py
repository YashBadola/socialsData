
import pytest
from socials_data.core.manager import PersonalityManager
from socials_data.core.loader import load_dataset
from pathlib import Path

PERSONALITY_ID = "soren_kierkegaard"

@pytest.fixture
def manager():
    return PersonalityManager()

def test_soren_kierkegaard_exists(manager):
    personalities = manager.list_personalities()
    assert PERSONALITY_ID in personalities

def test_soren_kierkegaard_metadata(manager):
    metadata = manager.get_metadata(PERSONALITY_ID)
    assert metadata["name"] == "Søren Kierkegaard"
    assert metadata["id"] == PERSONALITY_ID
    assert "existentialist" in metadata["description"].lower()
    assert "You are Søren Kierkegaard" in metadata["system_prompt"]
    assert len(metadata["sources"]) > 0

def test_soren_kierkegaard_dataset_structure(manager):
    # Check directory structure
    p_dir = manager.base_dir / PERSONALITY_ID
    assert (p_dir / "metadata.json").exists()
    assert (p_dir / "raw").exists()
    assert (p_dir / "processed").exists()
    assert (p_dir / "processed" / "data.jsonl").exists()

def test_soren_kierkegaard_content():
    # Load dataset
    dataset = load_dataset(PERSONALITY_ID)
    assert len(dataset) > 0

    # Check content of the first entry (or iterate to find specific content)
    found_keyword = False
    for item in dataset:
        text = item["text"]
        if "Knight of Faith" in text or "anxiety" in text.lower():
            found_keyword = True
            break

    assert found_keyword, "Expected keywords not found in the dataset text"
