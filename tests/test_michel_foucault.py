from socials_data import load_dataset
import pytest

def test_michel_foucault_dataset():
    # Load the dataset
    ds = load_dataset("michel_foucault")

    # Check if we have at least one item
    assert len(ds) >= 1

    # Check if the content is correct
    all_text = " ".join([item["text"] for item in ds])
    assert "In a system of discipline, the child is more individualized" in all_text
    # The text uses curly quotes: ‘docile’ bodies
    assert "docile" in all_text.lower()
    assert "bodies" in all_text.lower()
    assert "panopticism" not in all_text.lower()
    assert "disciplinary coercion establishes in the body" in all_text

if __name__ == "__main__":
    test_michel_foucault_dataset()
