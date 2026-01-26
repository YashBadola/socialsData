from socials_data import load_dataset
import pytest

def test_immanuel_kant_dataset():
    """Verify that the Immanuel Kant dataset loads correctly and contains expected content."""
    dataset = load_dataset("immanuel_kant")

    # We expect at least one item
    assert len(dataset) >= 1

    # Check if the content is correct
    all_text = " ".join([item["text"] for item in dataset])

    # Check for some characteristic phrases from the input text
    assert "Critique of Pure Reason" in all_text or "Pure and Empirical Knowledge" in all_text
    assert "knowledge begins with experience" in all_text
    assert "à priori" in all_text

    print("Immanuel Kant dataset test passed!")

if __name__ == "__main__":
    test_immanuel_kant_dataset()
