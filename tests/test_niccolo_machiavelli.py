import pytest
from socials_data.core.loader import load_dataset
from pathlib import Path
import json

def test_load_machiavelli_dataset():
    """Test that the Machiavelli dataset loads correctly."""
    try:
        dataset = load_dataset("niccolo_machiavelli")
    except Exception as e:
        pytest.fail(f"Failed to load dataset: {e}")

    assert len(dataset) > 0, "Dataset should not be empty"

    # Check first item
    item = dataset[0]
    assert "text" in item
    assert "source" in item
    assert item["source"] == "the_prince.txt"

    # Check for some keywords likely to be in The Prince
    text_content = " ".join([d["text"] for d in dataset])
    keywords = ["prince", "virtue", "fortune", "power", "state", "war"]
    found_keywords = [k for k in keywords if k in text_content.lower()]

    # We expect at least some of these keywords
    assert len(found_keywords) > 0, f"Expected keywords {keywords} not found in text."

def test_metadata_exists():
    """Test that metadata file exists and is valid."""
    metadata_path = Path("socials_data/personalities/niccolo_machiavelli/metadata.json")
    assert metadata_path.exists()

    with open(metadata_path, "r") as f:
        data = json.load(f)

    assert data["id"] == "niccolo_machiavelli"
    assert "Niccolò Machiavelli" in data["name"]
    assert "The Prince" in str(data["sources"])
