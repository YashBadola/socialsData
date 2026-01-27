from socials_data.core.loader import load_dataset
import pytest

def test_albert_camus_dataset():
    """
    Test loading the Albert Camus dataset.
    """
    ds = load_dataset("albert_camus")

    # We expect 3 items corresponding to the 3 raw files we added
    assert len(ds) == 3

    all_text = " ".join([item["text"] for item in ds])

    # Verify key phrases from our raw data
    assert "The Absurd is born of this confrontation" in all_text
    assert "One must imagine Sisyphus happy" in all_text
    assert "What is a rebel?" in all_text

if __name__ == "__main__":
    test_albert_camus_dataset()
