from socials_data import load_dataset
import pytest

def test_heraclitus_data():
    dataset = load_dataset("heraclitus")

    # Check if we have data
    assert len(dataset) > 0

    # Aggregate text
    all_text = " ".join([item["text"] for item in dataset])

    # Verify key phrases from our raw data exist
    assert "Panta Rhei" in all_text or "same river" in all_text
    assert "harmony of oppositions" in all_text
    assert "universal Reason" in all_text or "Logos" in all_text
    assert "ever living fire" in all_text

if __name__ == "__main__":
    test_heraclitus_data()
