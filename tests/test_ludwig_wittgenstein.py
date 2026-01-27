from socials_data import load_dataset
import pytest

def test_wittgenstein_load():
    # Load the dataset
    ds = load_dataset("ludwig_wittgenstein")

    # Check if we have at least one record
    assert len(ds) >= 1

    # Check if the content is correct
    text = ds[0]["text"]
    assert "Tractatus Logico-Philosophicus" in text
    assert "The world is all that is the case." in text
    assert "7 What we cannot speak about we must pass over in silence." in text

    print("Ludwig Wittgenstein dataset loaded successfully and verified!")

if __name__ == "__main__":
    test_wittgenstein_load()
