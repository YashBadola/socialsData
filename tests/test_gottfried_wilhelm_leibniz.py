from socials_data import load_dataset
import pytest

def test_leibniz_dataset():
    """Test that the Leibniz dataset loads and contains expected content."""
    ds = load_dataset("gottfried_wilhelm_leibniz")

    # Check that we have multiple items (paragraphs)
    assert len(ds) >= 90

    # Combine all text to check for terms coverage
    all_text = " ".join([item["text"] for item in ds]).lower()

    assert "monad" in all_text
    assert "simple substance" in all_text
    assert "sufficient reason" in all_text
    assert "preestablished harmony" in all_text.replace("-", "")

if __name__ == "__main__":
    test_leibniz_dataset()
