import os
import json
import pytest
from socials_data.core.loader import load_dataset

PERSONALITY_ID = "william_james"
# In the test environment, __file__ might be inside tests/.
# If we run from root with PYTHONPATH=., os.getcwd() is probably root.
# Let's try to find the root relative to this file.
# test file is at /app/tests/test_william_james.py
# so root is 1 level up.
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PERSONALITY_DIR = os.path.join(BASE_DIR, "socials_data", "personalities", PERSONALITY_ID)

def test_metadata_exists_and_valid():
    metadata_path = os.path.join(PERSONALITY_DIR, "metadata.json")
    assert os.path.exists(metadata_path)

    with open(metadata_path, 'r') as f:
        metadata = json.load(f)

    assert metadata['id'] == PERSONALITY_ID
    assert metadata['name'] == "William James"
    assert "system_prompt" in metadata
    assert len(metadata['sources']) == 3

def test_raw_files_exist():
    raw_dir = os.path.join(PERSONALITY_DIR, "raw")
    expected_files = [
        "pragmatism.txt",
        "varieties_of_religious_experience.txt",
        "will_to_believe.txt"
    ]
    for filename in expected_files:
        assert os.path.exists(os.path.join(raw_dir, filename))

def test_processed_data_loading():
    # Test loading via the loader
    dataset = load_dataset(PERSONALITY_ID)
    assert len(dataset) > 0

    # Check sample content
    sample = dataset[0]
    assert 'text' in sample
    assert 'source' in sample

    # Verify content from each book is present
    sources_found = set()
    for item in dataset:
        sources_found.add(item['source'])
        # Simple check to ensure content is meaningful (not just whitespace)
        assert len(item['text'].strip()) > 10

    expected_sources = {
        "pragmatism.txt",
        "varieties_of_religious_experience.txt",
        "will_to_believe.txt"
    }
    # Note: Depending on how load_dataset works, source might be full path or just filename.
    # Usually it's just filename if processed correctly.
    # Let's normalize to filename just in case
    normalized_sources = {os.path.basename(s) for s in sources_found}

    assert expected_sources.issubset(normalized_sources)

def test_content_keywords():
    dataset = load_dataset(PERSONALITY_ID)

    # Keywords that should appear in William James texts
    keywords = ["pragmatism", "religious", "belief", "truth"]

    found_keywords = {k: False for k in keywords}

    for item in dataset:
        text = item['text'].lower()
        for k in keywords:
            if k in text:
                found_keywords[k] = True

    for k, found in found_keywords.items():
        assert found, f"Keyword '{k}' not found in dataset"
