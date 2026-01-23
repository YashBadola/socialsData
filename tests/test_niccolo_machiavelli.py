from socials_data import load_dataset
import pytest

def test_machiavelli_dataset():
    # Verify we can load the data we just created
    ds = load_dataset("niccolo_machiavelli")

    # We added one big file, so there should be at least 1 item.
    assert len(ds) >= 1

    all_text = " ".join([item["text"] for item in ds])
    # The text uses "Nicolo" instead of "Niccolò"
    assert "Machiavelli" in all_text
    assert "The Prince" in all_text

if __name__ == "__main__":
    test_machiavelli_dataset()
