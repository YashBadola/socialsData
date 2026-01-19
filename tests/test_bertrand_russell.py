from socials_data import load_dataset
import pytest

def test_bertrand_russell():
    ds = load_dataset("bertrand_russell")
    assert len(ds) >= 2

    all_text = " ".join([item["text"] for item in ds])

    # Check for content from "The Problems of Philosophy"
    assert "The Problems of Philosophy" in all_text or "THE PROBLEMS OF PHILOSOPHY" in all_text

    # Check for content from "The Analysis of Mind"
    assert "The Analysis of Mind" in all_text or "THE ANALYSIS OF MIND" in all_text

if __name__ == "__main__":
    test_bertrand_russell()
