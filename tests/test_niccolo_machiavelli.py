import pytest
from socials_data.core.loader import load_dataset
from socials_data.core.manager import PersonalityManager

def test_load_niccolo_machiavelli():
    """Test that the Niccolò Machiavelli dataset loads correctly."""
    dataset = load_dataset("niccolo_machiavelli")
    assert len(dataset) > 0

    # Check sample content
    sample = dataset[0]
    assert "text" in sample
    assert isinstance(sample["text"], str)
    assert len(sample["text"]) > 0

    # Check metadata
    manager = PersonalityManager()
    metadata = manager.get_metadata("niccolo_machiavelli")
    assert metadata["name"] == "Niccolò Machiavelli"
    assert "The Prince" in str(metadata["sources"])

def test_content_keywords():
    """Verify that the content actually resembles Machiavelli."""
    dataset = load_dataset("niccolo_machiavelli")

    # Combine first few chunks to check for keywords
    # When slicing a Dataset, it returns a dict of lists (column-oriented)
    sliced_data = dataset[:5]
    text_content = " ".join(sliced_data["text"])

    keywords = ["prince", "state", "power", "virtu", "fortune", "italy", "florence", "duke", "arms", "people"]
    # Check that at least some keywords are present (case-insensitive)
    found_keywords = [k for k in keywords if k in text_content.lower()]
    assert len(found_keywords) > 0, f"Expected keywords not found in: {text_content[:200]}..."
