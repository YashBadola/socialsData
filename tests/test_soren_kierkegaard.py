import pytest
from socials_data.core.manager import PersonalityManager
import os
import json
from socials_data import load_dataset

def test_soren_kierkegaard_exists():
    manager = PersonalityManager()
    personalities = manager.list_personalities()
    assert "søren_kierkegaard" in personalities

def test_soren_kierkegaard_metadata():
    manager = PersonalityManager()
    metadata = manager.get_metadata("søren_kierkegaard")
    assert metadata["name"] == "Søren Kierkegaard"
    # Check for unicode ID
    assert metadata["id"] == "søren_kierkegaard"
    assert "The Sickness Unto Death" in [s["title"] for s in metadata["sources"]]

def test_soren_kierkegaard_data_loaded():
    dataset = load_dataset("søren_kierkegaard")
    assert len(dataset) > 0

    # Verify content
    found_poet = False
    for item in dataset:
        if "What is a poet?" in item["text"]:
            found_poet = True
            break

    assert found_poet, "Did not find the 'What is a poet?' excerpt."

def test_processed_file_content():
    processed_path = os.path.join("socials_data", "personalities", "søren_kierkegaard", "processed", "data.jsonl")
    assert os.path.exists(processed_path)

    with open(processed_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
        assert len(lines) == 3
