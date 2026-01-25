from socials_data import load_dataset
import pytest

def test_ludwig_wittgenstein_loading():
    # Load the dataset
    ds = load_dataset("ludwig_wittgenstein")

    # We added 2 lines in data.jsonl
    assert len(ds) == 2

    # Check content
    all_text = " ".join([item["text"] for item in ds])

    # Check for Tractatus content
    assert "The world is all that is the case" in all_text
    assert "Whereof one cannot speak, thereof one must be silent" in all_text

    # Check for Investigations content
    assert "meaning of a word is its use in the language" in all_text
    assert "fly-bottle" in all_text

if __name__ == "__main__":
    test_ludwig_wittgenstein_loading()
