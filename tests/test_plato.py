
import pytest
from socials_data.core.loader import load_dataset
from socials_data.core.manager import PersonalityManager

def test_plato_dataset_loading():
    """Test that the Plato dataset loads correctly."""
    try:
        dataset = load_dataset("plato")
    except Exception as e:
        pytest.fail(f"Failed to load dataset: {e}")

    assert len(dataset) > 0
    assert "text" in dataset[0]
    assert "source" in dataset[0]

    # Check for content relevance
    sample_text = dataset[0]["text"]
    assert isinstance(sample_text, str)
    assert len(sample_text) > 0

    # Check source
    assert "republic.txt" in dataset[0]["source"]

def test_plato_metadata():
    """Test that metadata loads correctly."""
    manager = PersonalityManager()
    metadata = manager.get_metadata("plato")

    assert metadata["name"] == "Plato"
    assert "The Republic" in [s["title"] for s in metadata["sources"]]
    assert metadata["id"] == "plato"
