
import pytest
from socials_data.core.loader import load_dataset
from socials_data.core.manager import PersonalityManager
import os

def test_voltaire_dataset_loading():
    """Test if the Voltaire dataset can be loaded successfully."""
    dataset = load_dataset("voltaire")
    assert len(dataset) > 0
    assert "text" in dataset[0]

    # Check if content from raw files is present
    texts = [item["text"] for item in dataset]
    assert any("Baron Thunder-ten-tronckh" in text for text in texts)
    assert any("English Parliament" in text for text in texts)
    assert any("Pure democracy" in text for text in texts)

def test_voltaire_metadata():
    """Test if Voltaire metadata is correct."""
    manager = PersonalityManager()

    # There is no get_personality_path, but we can assume the path or just check metadata
    # or access .base_dir
    personality_path = manager.base_dir / "voltaire"
    assert personality_path.exists()

    metadata = manager.get_metadata("voltaire")
    assert metadata["name"] == "Voltaire"
    assert metadata["id"] == "voltaire"
    assert len(metadata["sources"]) == 3
