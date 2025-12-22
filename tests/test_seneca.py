
import pytest
from socials_data import load_dataset

def test_load_seneca_dataset():
    """Test loading the Seneca dataset."""
    ds = load_dataset("seneca")
    assert len(ds) > 0
    assert "text" in ds[0]

    # Check for some keywords likely to appear in Seneca's Morals
    content = ds[0]["text"]
    keywords = ["virtue", "life", "Stoic", "Seneca", "happy", "death", "reason", "nature", "morals"]

    # Since the text is huge and chunking might vary, we just check if *some* keywords are present in the whole text (if it's one chunk)
    # or just check validity. The current processor seems to put the whole file in one entry if not chunked by Q&A generator.

    found_any = any(keyword in content.lower() for keyword in keywords)
    assert found_any, "Expected to find common Seneca keywords in the text."

def test_seneca_metadata_structure():
    """Test that metadata fields are correct."""
    import json
    import os

    metadata_path = "socials_data/personalities/seneca/metadata.json"
    assert os.path.exists(metadata_path)

    with open(metadata_path, "r") as f:
        metadata = json.load(f)

    assert metadata["id"] == "seneca"
    assert metadata["name"] == "Lucius Annaeus Seneca"
    assert "system_prompt" in metadata
    assert len(metadata["sources"]) > 0
