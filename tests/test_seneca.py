
import pytest
from socials_data.core.loader import load_dataset
from socials_data.core.manager import PersonalityManager

def test_seneca_dataset_loads():
    dataset = load_dataset("seneca")
    assert len(dataset) > 0
    # Check first item
    first_item = dataset[0]
    assert "text" in first_item
    assert "source" in first_item
    assert len(first_item["text"]) > 0

def test_seneca_metadata():
    manager = PersonalityManager()
    metadata = manager.get_metadata("seneca")
    assert metadata["name"] == "Lucius Annaeus Seneca"
    assert metadata["id"] == "seneca"
    assert "Stoic" in metadata["system_prompt"]
    assert metadata["sources"][0]["type"] == "book"

def test_seneca_content_keywords():
    dataset = load_dataset("seneca")
    # Join some text to check for keywords
    # We take a sample to avoid loading everything into memory if huge, but here it's small enough or we iterate.
    found_virtue = False
    found_reason = False

    # Check first 100 entries
    for i in range(min(len(dataset), 100)):
        text = dataset[i]["text"].lower()
        if "virtue" in text:
            found_virtue = True
        if "reason" in text or "nature" in text:
            found_reason = True

    assert found_virtue, "Text should contain 'virtue'"
    assert found_reason, "Text should contain 'reason' or 'nature'"
