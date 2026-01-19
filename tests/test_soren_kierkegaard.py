from socials_data.core.loader import load_dataset
import pytest

def test_load_soren_kierkegaard_dataset():
    """Test loading the Søren Kierkegaard dataset."""
    try:
        dataset = load_dataset("søren_kierkegaard")
    except ValueError as e:
        pytest.fail(f"Failed to load dataset: {e}")

    assert len(dataset) > 0, "Dataset should not be empty"

    # Check if the text content matches one of our expected excerpts
    # Since load_dataset returns a Hugging Face dataset, we access it like a list/dict
    first_entry = dataset[0]
    assert "text" in first_entry
    assert "source" in first_entry

    # Check if sources are correct
    sources = {item["source"] for item in dataset}
    expected_sources = {
        "sickness_unto_death_excerpt.txt",
        "either_or_excerpt.txt",
        "fear_and_trembling_excerpt.txt"
    }

    assert sources.issubset(expected_sources), f"Found unexpected sources: {sources - expected_sources}"
    assert expected_sources.issubset(sources), f"Missing sources: {expected_sources - sources}"
