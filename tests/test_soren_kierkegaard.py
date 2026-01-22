from socials_data.core.loader import load_dataset
import pytest

def test_soren_kierkegaard_dataset_exists():
    """Test that the Soren Kierkegaard dataset can be loaded."""
    try:
        dataset = load_dataset("soren_kierkegaard")
    except Exception as e:
        pytest.fail(f"Failed to load dataset: {e}")

    assert dataset is not None
    assert len(dataset) > 0

    # Check if the text content matches some expected key phrases
    found_phrase = False
    for item in dataset:
        if "Anxiety is the dizziness of freedom" in item['text']:
            found_phrase = True
            break

    assert found_phrase, "Key phrase not found in dataset"
