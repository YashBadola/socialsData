from socials_data import load_dataset
import pytest

def test_soren_kierkegaard():
    ds = load_dataset("soren_kierkegaard")
    assert len(ds) == 2
    all_text = " ".join([item["text"] for item in ds])
    assert "The Story of Abraham" in all_text
    assert "What is a poet?" in all_text
    print("Soren Kierkegaard test passed!")

if __name__ == "__main__":
    test_soren_kierkegaard()
