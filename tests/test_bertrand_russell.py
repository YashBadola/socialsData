from socials_data import load_dataset
import pytest

def test_bertrand_russell():
    ds = load_dataset("bertrand_russell")
    assert len(ds) >= 3
    all_text = " ".join([item["text"] for item in ds])
    assert "The Problems of Philosophy" in all_text or "appearance and reality" in all_text.lower()
    assert "The Analysis of Mind" in all_text or "introspection" in all_text.lower()
    assert "Mysticism and Logic" in all_text or "mysticism" in all_text.lower()

if __name__ == "__main__":
    test_bertrand_russell()
