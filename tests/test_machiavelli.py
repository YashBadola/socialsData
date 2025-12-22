from socials_data import load_dataset
import pytest

def test_load_machiavelli():
    """Test that the Niccolò Machiavelli dataset loads correctly."""
    dataset = load_dataset("niccolo_machiavelli")
    assert len(dataset) > 0
    assert "text" in dataset[0]

    # Check for keywords related to Machiavelli in at least one sample
    keywords = ["Prince", "virtue", "fortune", "state", "arms"]
    found = False
    for sample in dataset:
        text = sample["text"]
        if any(keyword in text for keyword in keywords):
            found = True
            break
    assert found, "Keywords not found in dataset"
