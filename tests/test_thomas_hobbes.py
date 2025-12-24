import os
import pytest
from socials_data.core.loader import load_dataset
from socials_data.core.manager import PersonalityManager

def test_hobbes_personality_exists():
    manager = PersonalityManager()
    personalities = manager.list_personalities()
    assert "thomas_hobbes" in personalities

def test_hobbes_metadata():
    manager = PersonalityManager()
    metadata = manager.get_metadata("thomas_hobbes")
    assert metadata["name"] == "Thomas Hobbes"
    assert "Leviathan" in [s["title"] for s in metadata["sources"]]
    assert "solitary, poor, nasty, brutish, and short" in metadata["system_prompt"]

def test_hobbes_dataset_loading():
    # Ensure processed file exists
    processed_path = os.path.join("socials_data", "personalities", "thomas_hobbes", "processed", "data.jsonl")
    assert os.path.exists(processed_path)

    # Load dataset
    dataset = load_dataset("thomas_hobbes")
    assert len(dataset) > 0

    # Check sample content
    sample = dataset[0]
    assert "text" in sample
    assert "source" in sample
    assert sample["source"] == "leviathan.txt"

    # Verify content relevance
    text_content = " ".join([d["text"] for d in dataset])
    assert "Leviathan" in text_content or "Common-wealth" in text_content
    assert "Soveraign" in text_content # Archaic spelling often used

    # Verify no license text (negative assertion)
    assert "Project Gutenberg License" not in text_content
