from socials_data import load_dataset
import pytest

def test_bertrand_russell_load():
    ds = load_dataset("bertrand_russell")
    assert len(ds) == 4

    # Check for presence of key concepts from the books
    all_text = " ".join([item["text"] for item in ds])

    # Problems of Philosophy
    assert "appearance and reality" in all_text.lower()

    # Analysis of Mind
    assert "sensation" in all_text.lower()

    # Mysticism and Logic
    assert "mysticism" in all_text.lower()

    # Proposed Roads to Freedom
    assert "socialism" in all_text.lower() or "anarchism" in all_text.lower()

if __name__ == "__main__":
    test_bertrand_russell_load()
