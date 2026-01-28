from socials_data import load_dataset
import pytest

def test_aristotle_dataset():
    # Load the aristotle dataset
    ds = load_dataset("aristotle")

    # We added 3 chunks of text (Ethics, Politics, Poetics)
    assert len(ds) == 3

    # Check for content from each
    all_text = " ".join([item["text"] for item in ds])

    # Ethics
    assert "mean between two vices" in all_text

    # Politics
    assert "political animal" in all_text

    # Poetics
    assert "imitation of an action" in all_text

if __name__ == "__main__":
    try:
        test_aristotle_dataset()
        print("Test passed!")
    except AssertionError as e:
        print(f"Test failed: {e}")
        exit(1)
    except Exception as e:
        print(f"An error occurred: {e}")
        exit(1)
