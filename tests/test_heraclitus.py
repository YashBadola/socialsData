from socials_data import load_dataset
import pytest

def test_heraclitus_dataset():
    # Load the Heraclitus dataset
    dataset = load_dataset("heraclitus")

    # Check that we have 6 items (corresponding to the 6 raw files we created)
    assert len(dataset) == 6

    # Collect all text to verify specific fragments
    all_text = " ".join([item["text"] for item in dataset])

    # specific checks for known fragments
    assert "Into the same river you could not step twice" in all_text
    assert "Nature loves to conceal herself" in all_text
    assert "War is the father and king of all" in all_text
    assert "The dry soul is the wisest and best" in all_text
    assert "Homer deserved to be driven out of the lists and flogged" in all_text

if __name__ == "__main__":
    test_heraclitus_dataset()
