import pytest
from socials_data.core.manager import PersonalityManager
import os
import json

def test_arthur_schopenhauer_dataset():
    """
    Test that the Arthur Schopenhauer dataset is correctly set up and processed.
    """
    manager = PersonalityManager()
    personality_id = "arthur_schopenhauer"

    # 1. Check Metadata
    metadata = manager.get_metadata(personality_id)
    assert metadata["name"] == "Arthur Schopenhauer"
    assert "pessimistic" in metadata["system_prompt"]
    assert len(metadata["sources"]) == 3

    # 2. Check Processed Data
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    processed_file = os.path.join(base_dir, "socials_data", "personalities", personality_id, "processed", "data.jsonl")

    assert os.path.exists(processed_file), "processed/data.jsonl does not exist"

    with open(processed_file, "r") as f:
        lines = f.readlines()

    assert len(lines) > 100, "Dataset should have a reasonable number of chunks"

    # Check a sample entry
    sample = json.loads(lines[0])
    assert "text" in sample
    assert "source" in sample
    assert isinstance(sample["text"], str)
    assert len(sample["text"]) > 0

    # 3. Check for specific content (random check)
    # Search for "will" or "suffering" which are key Schopenhauer themes
    found_keyword = False
    for line in lines[:100]:
        data = json.loads(line)
        text = data["text"].lower()
        if "will" in text or "suffering" in text or "pessimism" in text:
            found_keyword = True
            break

    assert found_keyword, "Did not find expected keywords in the first 100 chunks"
