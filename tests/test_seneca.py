from socials_data import load_dataset
import pytest

def test_seneca():
    ds = load_dataset("seneca")
    assert len(ds) == 5
    all_text = " ".join([item["text"] for item in ds])
    assert "Lucilius" in all_text
    assert "Seneca" in all_text
    print("Seneca test passed!")

if __name__ == "__main__":
    test_seneca()
