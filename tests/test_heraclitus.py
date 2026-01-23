from socials_data import load_dataset
import pytest

def test_heraclitus_dataset():
    # Load the dataset
    ds = load_dataset("heraclitus")

    # Check it's not empty
    assert len(ds) == 4, f"Expected 4 items, got {len(ds)}"

    # Concatenate all text
    all_text = " ".join([item["text"] for item in ds])

    # Check for key themes
    assert "Logos" in all_text
    assert "rivers" in all_text
    assert "Fire" in all_text
    assert "Ephesians" in all_text
    assert ("struggle" in all_text) or ("strife" in all_text)

    print("Heraclitus dataset test passed!")

if __name__ == "__main__":
    test_heraclitus_dataset()
