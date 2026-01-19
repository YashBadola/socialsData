from socials_data import load_dataset

def test_soren_kierkegaard():
    # Verify we can load the data we just created
    ds = load_dataset("soren_kierkegaard")

    # We have at least one big text chunk from the gutenberg file
    assert len(ds) >= 1

    all_text = " ".join([item["text"] for item in ds])

    # Check for some characteristic phrases from the "Selections" text
    assert "Abraham" in all_text
    assert "Mount Moriah" in all_text
    assert "The Present Moment" in all_text

    print("Soren Kierkegaard test passed!")

if __name__ == "__main__":
    test_soren_kierkegaard()
