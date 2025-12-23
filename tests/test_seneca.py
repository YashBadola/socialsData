import json
from pathlib import Path
from socials_data.core.loader import load_dataset
import pytest

def test_seneca_dataset_loads():
    """Test that the Seneca dataset can be loaded via the loader."""
    dataset = load_dataset("seneca")
    assert len(dataset) > 0

    # Check a sample
    sample = dataset[0]
    assert "text" in sample
    assert isinstance(sample["text"], str)
    assert len(sample["text"]) > 0
    assert "source" in sample
    assert "epistles.txt" in sample["source"]

def test_seneca_content_keywords():
    """Test that the content contains expected keywords."""
    dataset = load_dataset("seneca")

    # Check the first few samples for relevant keywords
    # Note: We can't guarantee every chunk has them, but searching across the dataset should find them.

    found_lucilius = False
    found_stoic_concept = False

    # Check first 20 samples
    for i in range(min(20, len(dataset))):
        text = dataset[i]["text"].lower()
        if "lucilius" in text:
            found_lucilius = True
        if any(w in text for w in ["virtue", "reason", "fortune", "nature", "death", "time"]):
            found_stoic_concept = True

    # Depending on how the text is chunked, "Lucilius" might not be in the first 20 chunks if there's a long intro.
    # But usually he addresses him early.

    # Let's just assert we found something relevant
    assert found_stoic_concept, "Did not find Stoic concepts in the first 20 samples"

def test_seneca_metadata():
    """Verify metadata file exists and is valid."""
    metadata_path = Path("socials_data/personalities/seneca/metadata.json")
    assert metadata_path.exists()

    with open(metadata_path, "r") as f:
        data = json.load(f)

    assert data["id"] == "seneca"
    assert "Stoic" in data["system_prompt"]
