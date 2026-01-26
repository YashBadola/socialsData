import pytest
from socials_data.core.loader import load_dataset
from socials_data.core.manager import PersonalityManager
import json
from pathlib import Path

def test_load_dataset():
    dataset = load_dataset("soren_kierkegaard")
    assert len(dataset) > 0
    assert "text" in dataset[0]
    assert "source" in dataset[0]

    # Check for content specific to Kierkegaard
    found_keyword = False
    for item in dataset:
        if "Knight of Faith" in item["text"] or "despair" in item["text"]:
            found_keyword = True
            break
    assert found_keyword, "Did not find expected keywords (Knight of Faith, despair) in the dataset"

def test_metadata():
    manager = PersonalityManager()
    metadata = manager.get_metadata("soren_kierkegaard")
    assert metadata["name"] == "Søren Kierkegaard"
    assert metadata["id"] == "soren_kierkegaard"
    assert metadata["sources"][0]["title"] == "Fear and Trembling"

def test_qa_dataset():
    # Construct path to qa.jsonl
    manager = PersonalityManager()
    personality_dir = manager.base_dir / "soren_kierkegaard"
    qa_file = personality_dir / "processed" / "qa.jsonl"

    assert qa_file.exists(), "qa.jsonl does not exist"

    with open(qa_file, "r") as f:
        lines = f.readlines()
        assert len(lines) >= 5

        for line in lines:
            data = json.loads(line)
            assert "instruction" in data
            assert "response" in data
            assert "source" in data
            assert isinstance(data["instruction"], str)
            assert isinstance(data["response"], str)

    # Check content of one QA pair
    first_qa = json.loads(lines[0])
    assert "teleological suspension" in first_qa["instruction"] or "teleological suspension" in first_qa["response"]
