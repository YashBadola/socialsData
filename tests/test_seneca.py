import pytest
from socials_data.core.manager import PersonalityManager
from socials_data.core.processor import TextDataProcessor
from pathlib import Path
import json

def test_seneca_exists():
    manager = PersonalityManager()
    personalities = manager.list_personalities()
    assert "lucius_annaeus_seneca" in personalities

def test_seneca_data_integrity():
    manager = PersonalityManager()
    personality_dir = manager.base_dir / "lucius_annaeus_seneca"
    processed_file = personality_dir / "processed" / "data.jsonl"

    assert processed_file.exists()

    with open(processed_file, "r") as f:
        lines = f.readlines()
        assert len(lines) > 0

        first_entry = json.loads(lines[0])
        assert "text" in first_entry
        assert "source" in first_entry
        assert "Seneca" in first_entry["text"]
