import json
from pathlib import Path
from socials_data.core.loader import load_dataset
import pytest

def test_leibniz_dataset_loads():
    """Test that the Leibniz dataset can be loaded via the loader."""
    dataset = load_dataset("gottfried_wilhelm_leibniz")
    assert len(dataset) > 0

    # Check a sample
    sample = dataset[0]
    assert "text" in sample
    assert isinstance(sample["text"], str)
    assert len(sample["text"]) > 0
    assert "source" in sample
    assert "monadology.txt" in sample["source"]

def test_leibniz_content_keywords():
    """Test that the content contains expected keywords."""
    dataset = load_dataset("gottfried_wilhelm_leibniz")

    found_monad = False
    found_sufficient_reason = False

    # Check samples (we only have 1 chunk currently, but iterating is good practice)
    for i in range(len(dataset)):
        text = dataset[i]["text"].lower()
        if "monad" in text:
            found_monad = True
        if "sufficient reason" in text:
            found_sufficient_reason = True

    assert found_monad, "Did not find 'monad' in the text."
    assert found_sufficient_reason, "Did not find 'sufficient reason' in the text."

def test_leibniz_metadata():
    """Verify metadata file exists and is valid."""
    metadata_path = Path("socials_data/personalities/gottfried_wilhelm_leibniz/metadata.json")
    assert metadata_path.exists()

    with open(metadata_path, "r") as f:
        data = json.load(f)

    assert data["id"] == "gottfried_wilhelm_leibniz"
    assert "Monadology" in data["sources"][0]["title"]
    assert "Sufficient Reason" in data["system_prompt"]
