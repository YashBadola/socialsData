from socials_data import load_dataset
import pytest

def test_diogenes_workflow():
    # Verify we can load the data for Diogenes
    ds = load_dataset("diogenes_of_sinope")

    # We expect at least one item
    assert len(ds) >= 1

    all_text = " ".join([item["text"] for item in ds])

    # Check for some known content
    assert "citizen of the world" in all_text
    assert "featherless biped" in all_text
    assert "stand a little out of my sun" in all_text

if __name__ == "__main__":
    test_diogenes_workflow()
