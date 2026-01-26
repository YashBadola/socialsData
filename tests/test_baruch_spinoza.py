import pytest
from socials_data.core.manager import PersonalityManager
import os
import json
from pathlib import Path

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
    assert "Deus sive Natura" in metadata["system_prompt"]

def test_baruch_spinoza_data_loaded():
    # Note: load_dataset requires the package to be installed or the path to be correct.
    # We test the processed file directly to avoid Hugging Face cache issues in test environment
    # or dependency on 'datasets' if it behaves weirdly with local paths.
    # However, let's try to simulate what load_dataset does.

    processed_path = Path("socials_data") / "personalities" / "baruch_spinoza" / "processed" / "data.jsonl"
    assert processed_path.exists()

    with open(processed_path, 'r') as f:
        lines = f.readlines()
        assert len(lines) > 0
        first_entry = json.loads(lines[0])
        assert "text" in first_entry
        assert "source" in first_entry
        assert first_entry["source"] == "ethics_part_1.txt"
        assert "CONCERNING GOD" in first_entry["text"]

def test_processed_file_content_structure():
    processed_path = os.path.join("socials_data", "personalities", "baruch_spinoza", "processed", "data.jsonl")
    assert os.path.exists(processed_path)

    with open(processed_path, 'r') as f:
        lines = f.readlines()
        assert len(lines) > 0
        first_entry = json.loads(lines[0])
        # Check that newline cleaning happened (the text should be one long string or have \n preserved?)
        # The processor collapses newlines but joins with \n.
        # "lines = [line.strip() for line in text.splitlines() if line.strip()]"
        # "cleaned_text = "\n".join(lines)"

        # Verify the text is not empty
        assert len(first_entry["text"]) > 100
