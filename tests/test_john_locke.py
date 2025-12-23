import json
import pytest
from pathlib import Path
from socials_data import load_dataset

def test_john_locke_personality_structure():
    base_dir = Path("socials_data/personalities/john_locke")

    # Check directory structure
    assert base_dir.exists()
    assert (base_dir / "metadata.json").exists()
    assert (base_dir / "raw").exists()
    assert (base_dir / "processed").exists()

    # Check metadata content
    with open(base_dir / "metadata.json", "r") as f:
        metadata = json.load(f)
        assert metadata["id"] == "john_locke"
        assert metadata["name"] == "John Locke"
        assert "system_prompt" in metadata
        assert len(metadata["sources"]) == 2

    # Check raw files
    raw_files = list((base_dir / "raw").glob("*.txt"))
    assert len(raw_files) == 2
    filenames = [f.name for f in raw_files]
    assert "second_treatise_of_government.txt" in filenames
    assert "an_essay_concerning_human_understanding.txt" in filenames

    # Check processed files
    assert (base_dir / "processed/data.jsonl").exists()

    # Check content of processed data
    with open(base_dir / "processed/data.jsonl", "r") as f:
        lines = f.readlines()
        assert len(lines) > 0

        first_entry = json.loads(lines[0])
        assert "text" in first_entry
        assert "source" in first_entry
        assert isinstance(first_entry["text"], str)

def test_load_dataset_john_locke():
    # Test loading via the package function
    ds = load_dataset("john_locke")
    assert len(ds) > 0

    # Check a sample
    sample = ds[0]
    assert "text" in sample
    assert "source" in sample

    # Check for some keywords in the dataset to verify content
    # Combine some text to search
    all_text = " ".join([entry["text"] for entry in ds])
    assert "Locke" in all_text or "LOCKE" in all_text # Should be in title or headers if preserved, or naturally
    assert "government" in all_text.lower()
    assert "understanding" in all_text.lower()
