import pytest
from socials_data.core.loader import load_dataset
from socials_data.core.manager import PersonalityManager

def test_load_leibniz_dataset():
    """Test loading the Gottfried Wilhelm Leibniz dataset."""
    try:
        dataset = load_dataset("gottfried_wilhelm_leibniz")
        assert len(dataset) > 0, "Dataset should not be empty"

        # Check if the text content matches what we expect
        first_entry = dataset[0]
        assert "text" in first_entry
        assert "Monad" in first_entry["text"] or "monad" in first_entry["text"]
    except Exception as e:
        pytest.fail(f"Failed to load dataset: {e}")

def test_leibniz_metadata():
    """Test that Leibniz metadata exists and is correct."""
    manager = PersonalityManager()
    metadata = manager.get_metadata("gottfried_wilhelm_leibniz")

    assert metadata["name"] == "Gottfried Wilhelm Leibniz"
    assert metadata["id"] == "gottfried_wilhelm_leibniz"
    assert "Monadology" in metadata["description"]
