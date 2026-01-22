
import pytest
from socials_data.core.loader import load_dataset
from socials_data.core.manager import PersonalityManager
import os

def test_soren_kierkegaard_exists():
    manager = PersonalityManager()
    personalities = manager.list_personalities()
    assert "soren_kierkegaard" in personalities

def test_soren_kierkegaard_metadata():
    manager = PersonalityManager()
    metadata = manager.get_metadata("soren_kierkegaard")
    assert metadata["name"] == "Søren Kierkegaard"
    assert metadata["id"] == "soren_kierkegaard"
    assert "existentialist" in metadata["description"]

def test_soren_kierkegaard_dataset_load():
    # Only verify if processed data exists
    manager = PersonalityManager()
    path = manager.base_dir / "soren_kierkegaard" / "processed" / "data.jsonl"
    if path.exists():
        dataset = load_dataset("soren_kierkegaard")
        assert len(dataset) > 0
        assert "text" in dataset[0]
        # Check if some characteristic text is present
        texts = [row["text"] for row in dataset]
        combined_text = " ".join(texts)
        assert "Anxiety" in combined_text or "existential" in combined_text or "silence" in combined_text
