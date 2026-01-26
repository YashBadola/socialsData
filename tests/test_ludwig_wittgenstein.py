from socials_data import load_dataset
import pytest

def test_ludwig_wittgenstein():
    ds = load_dataset("ludwig_wittgenstein")

    # We populated it with roughly 38 items (19 from each text file)
    # Let's verify we have at least that many.
    assert len(ds) >= 30

    all_text = " ".join([item["text"] for item in ds])

    # Check for specific quotes from Tractatus
    assert "The world is all that is the case." in all_text
    assert "Whereof one cannot speak, thereof one must be silent." in all_text

    # Check for specific quotes from Investigations
    assert "If a lion could speak, we could not understand him." in all_text
    assert "language games" in all_text or "language goes on holiday" in all_text

    print("Ludwig Wittgenstein test passed!")

if __name__ == "__main__":
    test_ludwig_wittgenstein()
