import pytest
from socials_data.core.loader import load_dataset
from pathlib import Path

def test_simone_de_beauvoir_structure():
    base_dir = Path("socials_data/personalities/simone_de_beauvoir")
    assert (base_dir / "raw").exists()
    assert (base_dir / "processed").exists()
    assert (base_dir / "metadata.json").exists()
    assert (base_dir / "processed" / "philosophy.db").exists()
    assert (base_dir / "processed" / "data.jsonl").exists()

def test_simone_de_beauvoir_load():
    dataset = load_dataset("simone_de_beauvoir")
    assert len(dataset) > 0
    entry = dataset[0]
    assert "text" in entry
    assert "source" in entry
    assert "metadata" in entry
    assert "sentiment" in entry["metadata"]
