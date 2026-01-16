from socials_data.core.loader import load_dataset
import pytest

def test_load_soren_kierkegaard_dataset():
    """Test loading the Soren Kierkegaard dataset."""
    try:
        dataset = load_dataset("soren_kierkegaard")
    except ValueError as e:
        pytest.fail(f"Failed to load dataset: {e}")

    assert dataset is not None
    assert len(dataset) > 0

    # Check if the first entry contains text
    sample = dataset[0]
    assert "text" in sample
    assert isinstance(sample["text"], str)
    assert len(sample["text"]) > 0
    assert "source" in sample
    assert sample["source"] == "excerpts.txt"
