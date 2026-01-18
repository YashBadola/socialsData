from socials_data import load_dataset
import pytest

def test_diogenes_of_sinope_loading():
    """
    Test that the Diogenes of Sinope dataset can be loaded
    and contains the expected content.
    """
    try:
        # Load the dataset
        dataset = load_dataset("diogenes_of_sinope")

        # Check if dataset is not empty
        assert len(dataset) > 0, "Dataset should not be empty"

        # Check the first entry
        first_entry = dataset[0]
        assert "text" in first_entry, "Entry should contain 'text' field"
        assert "source" in first_entry, "Entry should contain 'source' field"
        assert "Diogenes" in first_entry["text"], "Text should contain reference to Diogenes"

    except FileNotFoundError:
        pytest.fail("Diogenes of Sinope dataset not found. Make sure it is processed.")
    except Exception as e:
        pytest.fail(f"Failed to load dataset: {e}")
