import pytest
from socials_data.core.manager import PersonalityManager
import os
import json

def test_baruch_spinoza_exists():
    manager = PersonalityManager()
    personalities = manager.list_personalities()
    assert "baruch_spinoza" in personalities

def test_baruch_spinoza_metadata():
    manager = PersonalityManager()
    metadata = manager.get_metadata("baruch_spinoza")
    assert metadata["name"] == "Baruch Spinoza"
    assert metadata["id"] == "baruch_spinoza"
    assert "Ethics" in [s["title"] for s in metadata["sources"]]

def test_baruch_spinoza_data_loaded():
    from socials_data import load_dataset
    dataset = load_dataset("baruch_spinoza")
    assert len(dataset) > 0

    # Check that we have multiple entries (since we had 3 source files)
    # The processor iterates files, so each file becomes an entry unless chunks are split differently.
    # Based on the output I saw, it seems 1 line per file.
    assert len(dataset) >= 3

    # Check content
    text_content = [item["text"] for item in dataset]
    combined_text = " ".join(text_content)

    assert "Substance is by nature prior to its modifications" in combined_text
    assert "By that which is self-caused" in combined_text
    assert "Everything which exists, exists either in itself or in something else" in combined_text

def test_processed_file_exists():
    processed_path = os.path.join("socials_data", "personalities", "baruch_spinoza", "processed", "data.jsonl")
    assert os.path.exists(processed_path)
