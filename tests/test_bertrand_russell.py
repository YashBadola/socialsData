from socials_data import load_dataset
import pytest

def test_bertrand_russell():
    # Verify we can load the data we just created
    ds = load_dataset("bertrand_russell")
    assert len(ds) >= 1

    # Check content
    all_text = " ".join([item["text"] for item in ds])
    assert "THE PROBLEMS OF PHILOSOPHY" in all_text
    assert "appearance" in all_text.lower()
    assert "reality" in all_text.lower()

if __name__ == "__main__":
    test_bertrand_russell()
