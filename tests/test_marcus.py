import pytest
import os
import json
from pathlib import Path
from socials_data.core.manager import PersonalityManager
from socials_data.core.processor import TextDataProcessor

def test_marcus_aurelius_exists():
    manager = PersonalityManager()
    personalities = manager.list_personalities()
    assert "marcus_aurelius" in personalities

def test_marcus_aurelius_metadata():
    manager = PersonalityManager()
    meta = manager.get_metadata("marcus_aurelius")
    assert meta["name"] == "Marcus Aurelius"
    assert "Meditations" in [s["title"] for s in meta["sources"]]

def test_marcus_aurelius_processing(tmp_path):
    # This test verifies that we can process the data.
    # Note: We are running this on the actual data, so it might take a moment.
    # We won't test Q&A generation here as it requires an API key and mocks.

    manager = PersonalityManager()
    processor = TextDataProcessor()

    personality_dir = manager.base_dir / "marcus_aurelius"
    processed_dir = personality_dir / "processed"
    output_file = processed_dir / "data.jsonl"

    # Clean up previous run if any
    if output_file.exists():
        output_file.unlink()

    # Run processing (only for text data, Q&A will be skipped if no API key)
    processor.process(personality_dir)

    assert output_file.exists()

    with open(output_file, "r") as f:
        lines = f.readlines()
        assert len(lines) > 0
        first_entry = json.loads(lines[0])
        assert "text" in first_entry
        assert "source" in first_entry
        assert first_entry["source"] == "meditations.txt"
