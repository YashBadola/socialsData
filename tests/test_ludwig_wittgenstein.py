from socials_data import load_dataset
import pytest

def test_ludwig_wittgenstein_dataset():
    # Verify we can load the data we just created
    ds = load_dataset("ludwig_wittgenstein")

    # We expect 2 items (tractatus and investigations files)
    assert len(ds) == 2

    all_text = " ".join([item["text"] for item in ds])

    # Check for Tractatus content
    assert "The world is everything that is the case" in all_text
    assert "Whereof one cannot speak, thereof one must be silent" in all_text

    # Check for Investigations content
    assert "Meaning is use" in all_text
    assert "beetle in a box" in all_text

if __name__ == "__main__":
    test_ludwig_wittgenstein_dataset()
