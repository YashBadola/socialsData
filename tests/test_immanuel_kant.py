import os
import json
import pytest
from socials_data.core.loader import load_dataset

PERSONALITY_ID = "immanuel_kant"
BASE_DIR = f"socials_data/personalities/{PERSONALITY_ID}"

def test_immanuel_kant_files_exist():
    assert os.path.exists(os.path.join(BASE_DIR, "metadata.json"))
    assert os.path.exists(os.path.join(BASE_DIR, "raw"))
    assert os.path.exists(os.path.join(BASE_DIR, "processed"))
    assert os.path.exists(os.path.join(BASE_DIR, "processed/data.jsonl"))

def test_immanuel_kant_metadata():
    with open(os.path.join(BASE_DIR, "metadata.json"), "r") as f:
        metadata = json.load(f)

    assert metadata["id"] == PERSONALITY_ID
    assert metadata["name"] == "Immanuel Kant"
    assert len(metadata["sources"]) == 5
    assert "System Prompt" not in metadata # Keys should be snake_case in this file usually? Wait, memory says `system_prompt`.
    assert "system_prompt" in metadata

def test_immanuel_kant_dataset_loads():
    # Load dataset
    ds = load_dataset(PERSONALITY_ID)
    assert len(ds) > 0

    # Check sample content
    sample = ds[0]
    assert "text" in sample
    assert "source" in sample

    # Check that sources map to expected filenames
    expected_sources = [
        "critique_of_pure_reason.txt",
        "critique_of_practical_reason.txt",
        "fundamental_principles_metaphysic_morals.txt",
        "metaphysical_elements_ethics.txt",
        "critique_of_judgement.txt"
    ]

    # Collect all unique sources found in the dataset
    found_sources = set(ds["source"])

    for source in expected_sources:
        assert source in found_sources

def test_immanuel_kant_content_keywords():
    ds = load_dataset(PERSONALITY_ID)

    # Keywords we expect to find across the corpus
    keywords = ["reason", "moral", "critique", "judgment", "ethics"]

    found_keywords = {k: False for k in keywords}

    for item in ds:
        text = item["text"].lower()
        for k in keywords:
            if k in text:
                found_keywords[k] = True

    assert all(found_keywords.values()), f"Missing keywords: {[k for k, v in found_keywords.items() if not v]}"
