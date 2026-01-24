import pytest
from socials_data.core.loader import load_dataset

def test_load_heraclitus_dataset():
    # Attempt to load the dataset
    try:
        ds = load_dataset("heraclitus")
    except ValueError:
        pytest.fail("Heraclitus dataset not found")

    assert len(ds) > 0, "Dataset should not be empty"

    # Check if we have some expected content
    found_river = False
    for row in ds:
        if "river" in row["text"].lower() or "waters" in row["text"].lower():
            found_river = True
            break

    assert found_river, "Should find river-related fragments in Heraclitus dataset"
