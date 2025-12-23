
import pytest
import os
from socials_data.core.manager import PersonalityManager
from socials_data.core.loader import load_dataset as loader_load_dataset

def test_plato_metadata():
    manager = PersonalityManager()
    metadata = manager.get_metadata("plato")

    assert metadata["name"] == "Plato"
    assert metadata["id"] == "plato"
    assert len(metadata["sources"]) == 2
    assert "The Republic" in [s["title"] for s in metadata["sources"]]
    assert "Symposium" in [s["title"] for s in metadata["sources"]]

def test_plato_processed_data_exists():
    processed_path = os.path.join("socials_data", "personalities", "plato", "processed", "data.jsonl")
    assert os.path.exists(processed_path)
    assert os.path.getsize(processed_path) > 0

def test_load_dataset_plato():
    dataset = loader_load_dataset("plato")
    assert dataset is not None
    # Depending on how load_dataset works, it might return a Dataset object or similar.
    # The memory said: "Verification tests for new personalities should assert that load_dataset returns a Hugging Face Dataset object"

    # Check if it has 'text' and 'source' columns
    sample = dataset[0]
    assert "text" in sample
    assert "source" in sample

    # Check content of a sample
    # We expect some text from The Republic or Symposium
    # The processed data usually chunks text.

    # Let's check if we can find a known phrase
    texts = dataset["text"]
    found_republic = False
    for t in texts[:100]: # Check first 100 chunks
        if "justice" in t.lower() or "socrates" in t.lower() or "glaucon" in t.lower():
            found_republic = True
            break
    assert found_republic, "Did not find expected keywords in the first 100 chunks"
