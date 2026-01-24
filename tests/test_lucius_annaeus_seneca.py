from socials_data import load_dataset
import pytest

def test_seneca_dataset():
    ds = load_dataset("lucius_annaeus_seneca")
    assert len(ds) > 0
    all_text = " ".join([item["text"] for item in ds])
    # "Liberalis" is addressed in On Benefits. "Clemency" is in the title of one book.
    # "Paulinus" is in On the Shortness of Life (often in Minor Dialogues).
    assert "Liberalis" in all_text or "Paulinus" in all_text or "Clemency" in all_text
    print("Seneca test passed!")

if __name__ == "__main__":
    test_seneca_dataset()
