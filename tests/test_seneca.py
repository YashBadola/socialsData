from socials_data.core.loader import load_dataset
from socials_data.core.manager import PersonalityManager
import pytest

def test_seneca_dataset():
    manager = PersonalityManager()
    personality_id = "seneca"

    # Check metadata
    metadata = manager.get_metadata(personality_id)
    assert metadata["name"] == "Lucius Annaeus Seneca"
    assert metadata["id"] == "seneca"

    # Check dataset loading
    dataset = load_dataset(personality_id)
    assert len(dataset) > 0

    # Check content of first item
    first_item = dataset[0]
    assert "text" in first_item
    assert "source" in first_item
    assert "Seneca" in first_item["text"] or "EPISTLE" in first_item["text"]
