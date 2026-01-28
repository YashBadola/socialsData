from socials_data import load_dataset
import pytest

def test_immanuel_kant_data():
    """
    Test that the Immanuel Kant dataset loads correctly and contains expected text.
    """
    # Load the dataset for Immanuel Kant
    dataset = load_dataset("immanuel_kant")

    # We expect 2 entries corresponding to our 2 raw files
    assert len(dataset) == 2

    # Collect all text
    all_text = " ".join([item["text"] for item in dataset])

    # Check for specific phrases from Critique of Pure Reason
    assert "Time is not an empirical concept" in all_text
    assert "universality of appearances possible" in all_text

    # Check for specific phrases from Groundwork
    assert "Act only according to that maxim" in all_text
    assert "kingdom of ends" in all_text

if __name__ == "__main__":
    test_immanuel_kant_data()
