from socials_data import load_dataset
import pytest

def test_wittgenstein():
    ds = load_dataset("ludwig_wittgenstein")
    assert len(ds) > 0
    all_text = " ".join([item["text"] for item in ds])
    assert "Tractatus Logico-Philosophicus" in all_text
    assert "Whereof one cannot speak, thereof one must be silent." in all_text
    print("Wittgenstein test passed!")

if __name__ == "__main__":
    test_wittgenstein()
