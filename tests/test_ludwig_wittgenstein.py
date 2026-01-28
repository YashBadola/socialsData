from socials_data import load_dataset
import pytest

def test_wittgenstein_dataset():
    # Load the dataset
    dataset = load_dataset("ludwig_wittgenstein")

    # Check that it's not empty
    assert len(dataset) > 0, "Dataset should not be empty"

    # Check for specific famous propositions
    texts = [item["text"] for item in dataset]
    # HF dataset items are dicts
    ids = [item.get("proposition_id") for item in dataset]

    assert "The world is all that is the case." in texts
    assert "1" in ids

    # Checking the final proposition (7)
    # The text I verified earlier: "What we cannot speak about we must pass over in silence."
    assert "What we cannot speak about we must pass over in silence." in texts
    assert "7" in ids

    # Check structure
    first_item = dataset[0]
    assert "text" in first_item
    assert "proposition_id" in first_item
    assert "source" in first_item

if __name__ == "__main__":
    test_wittgenstein_dataset()
