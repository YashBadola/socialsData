from socials_data import load_dataset
import pytest

def test_rousseau_loading():
    # Verify we can load the data for Jean-Jacques Rousseau
    ds = load_dataset("jean_jacques_rousseau")

    # Check that the dataset is not empty
    assert len(ds) > 0

    # Check content
    all_text = " ".join([item["text"] for item in ds])
    assert "The Social Contract" in all_text
    assert "MAN is born free; and everywhere he is in chains" in all_text
    assert "general will" in all_text

if __name__ == "__main__":
    test_rousseau_loading()
