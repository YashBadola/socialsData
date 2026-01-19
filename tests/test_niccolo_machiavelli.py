from socials_data import load_dataset
import pytest

def test_niccolo_machiavelli():
    # Verify we can load the data we just created
    ds = load_dataset("niccolo_machiavelli")

    # We added 2 text files, so there should be at least 2 items.
    assert len(ds) >= 2

    all_text = " ".join([item["text"] for item in ds])

    # Check for content from "The Prince"
    assert "The Prince" in all_text
    assert "Niccolò Machiavelli" in all_text

    # Check for content from "Discourses on Livy"
    assert "Discourses" in all_text
    assert "Titus Livius" in all_text

if __name__ == "__main__":
    test_niccolo_machiavelli()
