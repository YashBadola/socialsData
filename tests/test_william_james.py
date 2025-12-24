import os
import json
import pytest
from pathlib import Path
from socials_data.core.loader import load_dataset
from socials_data.core.manager import PersonalityManager

def test_william_james_exists():
    manager = PersonalityManager()
    personalities = manager.list_personalities()
    assert "william_james" in personalities

def test_william_james_metadata():
    manager = PersonalityManager()
    metadata = manager.get_metadata("william_james")
    assert metadata["name"] == "William James"
    assert metadata["id"] == "william_james"
    assert "Pragmatism" in metadata["system_prompt"]
    assert len(metadata["sources"]) == 4

def test_load_dataset_william_james():
    # Ensure processed data exists before loading
    dataset = load_dataset("william_james")
    assert dataset is not None
    # HuggingFace dataset behavior
    assert len(dataset) > 0

    # Check sample
    sample = dataset[0]
    assert "text" in sample
    assert "source" in sample
    assert isinstance(sample["text"], str)
    assert len(sample["text"]) > 0

    # Check for specific content to ensure it's not empty or garbage
    # We look for "pragmatism" or "religious" which should be common in his text
    found_keyword = False
    for i in range(min(len(dataset), 100)):
        text = dataset[i]["text"].lower()
        if "pragmatism" in text or "religious" in text or "psychology" in text or "experience" in text:
            found_keyword = True
            break
    assert found_keyword, "Did not find expected keywords in the first 100 samples"

def test_raw_files_exist():
    base_dir = Path("socials_data/personalities/william_james/raw")
    expected_files = [
        "pragmatism.txt",
        "varieties_religious_experience.txt",
        "principles_psychology_1.txt",
        "essays_radical_empiricism.txt"
    ]
    for f in expected_files:
        assert (base_dir / f).exists()

def test_processed_files_exist():
    base_dir = Path("socials_data/personalities/william_james/processed")
    assert (base_dir / "data.jsonl").exists()

def test_no_gutenberg_headers():
    # Verify that the cleaning script worked
    dataset = load_dataset("william_james")
    for i in range(min(len(dataset), 20)):
        text = dataset[i]["text"]
        assert "*** START OF THE PROJECT" not in text
        assert "Project Gutenberg" not in text[:500] # Should be gone from start
