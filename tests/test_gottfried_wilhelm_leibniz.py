from socials_data import load_dataset
import pytest

def test_leibniz_dataset_structure():
    ds = load_dataset("gottfried_wilhelm_leibniz")

    # Check if we have data
    assert len(ds) > 0

    # Check content
    all_text = " ".join([item["text"] for item in ds])
    assert "Monadology" in all_text
    assert "simple substance" in all_text
    assert "have no windows" in all_text
    assert "city of God" in all_text

if __name__ == "__main__":
    test_leibniz_dataset_structure()
