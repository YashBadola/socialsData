from socials_data import load_dataset
import pytest

def test_rene_descartes_load():
    """Test loading the Rene Descartes dataset."""
    try:
        dataset = load_dataset('rene_descartes')
    except ValueError as e:
        pytest.fail(f"Failed to load dataset: {e}")

    assert dataset is not None, "Dataset should not be None"
    assert len(dataset) > 0, "Dataset should not be empty"

    # Check for expected fields
    example = dataset[0]
    assert 'text' in example, "Dataset should contain 'text' field"
    assert 'source' in example, "Dataset should contain 'source' field"

    # Check content (brief check to ensure it's the right text)
    assert "DISCOURSE ON THE METHOD" in example['text'], "Text content mismatch"
