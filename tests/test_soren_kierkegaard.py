from socials_data.core.loader import load_dataset
import pytest

def test_load_soren_kierkegaard_dataset():
    """Test loading the Søren Kierkegaard dataset."""
    try:
        dataset = load_dataset("søren_kierkegaard")
    except ValueError as e:
        pytest.fail(f"Failed to load dataset: {e}")

    assert dataset is not None
    assert len(dataset) > 0

    # Check if the dataset has the expected columns
    # Assuming 'text' is a standard column, and 'source' might be there.
    assert "text" in dataset.column_names

    # Check content of the first entry
    first_entry = dataset[0]
    assert isinstance(first_entry['text'], str)
    assert len(first_entry['text']) > 0
