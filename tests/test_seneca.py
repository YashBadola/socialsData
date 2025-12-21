import pytest
import os
import json
from socials_data.core.manager import PersonalityManager

def test_seneca_dataset_exists():
    manager = PersonalityManager()
    personalities = manager.list_personalities()
    assert "seneca" in personalities

def test_seneca_metadata():
    manager = PersonalityManager()
    metadata = manager.get_metadata("seneca")
    assert metadata["name"] == "Seneca"
    assert "Stoic" in metadata["description"]
    assert "System Prompt" not in metadata  # The key is likely "system_prompt" but let's check dict
    assert "system_prompt" in metadata
    assert "sources" in metadata
    assert len(metadata["sources"]) > 0

def test_seneca_processed_data():
    manager = PersonalityManager()
    personality_dir = manager.base_dir / "seneca"
    data_file = personality_dir / "processed" / "data.jsonl"

    assert data_file.exists()

    # Read first few lines to check validity
    with open(data_file, 'r') as f:
        lines = [json.loads(line) for line in f.readlines()]

    assert len(lines) > 0
    assert "text" in lines[0]
    assert len(lines[0]["text"]) > 0
    # Check that not all lines are just Gutenberg license info (simple heuristic)
    # We can check if we have enough content.
    assert len(lines) > 10
