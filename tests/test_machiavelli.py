from socials_data import load_dataset
import pytest

def test_machiavelli():
    ds = load_dataset("niccolo_machiavelli")
    assert len(ds) > 0
    all_text = " ".join([item["text"] for item in ds])
    # Check for some keywords likely to be in The Prince
    assert "Prince" in all_text
    assert "Duke" in all_text
    print("Machiavelli test passed!")

if __name__ == "__main__":
    test_machiavelli()
