import pytest
from socials_data.core.loader import load_dataset
from pathlib import Path
import json

def test_load_machiavelli_dataset():
    """Test loading the Niccolò Machiavelli dataset."""
    try:
        dataset = load_dataset("niccolo_machiavelli")
    except Exception as e:
        pytest.fail(f"Failed to load dataset: {e}")

    assert len(dataset) > 0, "Dataset should have entries"

    # Check first item structure
    item = dataset[0]
    assert "text" in item
    assert "source" in item
    assert isinstance(item["text"], str)
    assert len(item["text"]) > 0

    # Verify content keywords
    text_content = " ".join([d["text"] for d in dataset])
    assert "Prince" in text_content or "Republic" in text_content or "Italy" in text_content
    assert "Machiavelli" in text_content or "Medici" in text_content

def test_machiavelli_metadata():
    """Test metadata for Niccolò Machiavelli."""
    metadata_path = Path("socials_data/personalities/niccolo_machiavelli/metadata.json")
    assert metadata_path.exists()

    with open(metadata_path, "r") as f:
        metadata = json.load(f)

    assert metadata["name"] == "Niccolò Machiavelli"
    assert metadata["id"] == "niccolo_machiavelli"
    assert "system_prompt" in metadata
    assert len(metadata["sources"]) == 2
