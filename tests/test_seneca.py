from socials_data import load_dataset
import pytest

def test_seneca_dataset():
    ds = load_dataset("seneca")
    assert len(ds) > 0

    all_text = " ".join([item["text"] for item in ds])

    # Check for keywords from the raw data I added
    assert "not that we have so little time" in all_text
    assert "Amor Fati" not in all_text # I didn't add this explicitly in the text file, only in metadata system prompt.
    assert "Associate with people who are likely to improve you" in all_text

if __name__ == "__main__":
    test_seneca_dataset()
