from socials_data import load_dataset
import pytest

def test_ludwig_wittgenstein():
    ds = load_dataset("ludwig_wittgenstein")
    assert len(ds) >= 1
    all_text = " ".join([item["text"] for item in ds])

    # Check for title
    assert "Tractatus Logico-Philosophicus" in all_text

    # Check for famous proposition 7
    # Note: The text file has newlines, so we check for substring carefully or normalized
    assert "What we cannot speak about we must pass over in silence" in all_text

if __name__ == "__main__":
    test_ludwig_wittgenstein()
