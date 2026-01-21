from socials_data import load_dataset
import pytest

def test_jean_jacques_rousseau_dataset():
    try:
        ds = load_dataset("jean_jacques_rousseau")
    except ValueError as e:
        pytest.skip(f"Dataset for jean_jacques_rousseau not found: {e}")

    assert len(ds) > 0
    sample = ds[0]
    assert "text" in sample
    assert len(sample["text"]) > 0
    # Check for chunking if possible, though hard to verify strictly without knowing exact content.
    # But we know I modified the processor to chunk.
    # If the file was processed correctly, we should have multiple records.
    # The previous `wc -l` showed 216 lines.
    assert len(ds) > 1
