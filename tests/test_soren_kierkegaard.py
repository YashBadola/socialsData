import pytest
from socials_data import load_dataset
from socials_data.core.manager import PersonalityManager

def test_soren_kierkegaard_dataset():
    # Load the dataset
    ds = load_dataset("søren_kierkegaard")

    # Check if there are 4 entries (since we created 4 files)
    assert len(ds) == 4

    # Collect all text to verify content
    all_text = " ".join([item["text"] for item in ds])

    # Check for specific phrases from our raw data
    assert "The ethical expression for what Abraham did is that he would murder Isaac" in all_text
    assert "Anxiety is the dizziness of freedom" in all_text
    assert "The sickness unto death is despair" in all_text
    assert "Marry, and you will regret it" in all_text

    # Verify metadata
    manager = PersonalityManager()
    meta = manager.get_metadata("søren_kierkegaard")
    assert meta["name"] == "Søren Kierkegaard"
    assert meta["id"] == "soren_kierkegaard"
