from socials_data import load_dataset

def test_ralph_waldo_emerson():
    # Verify we can load the data we just created
    ds = load_dataset("ralph_waldo_emerson")
    # We added new content, so now there should be 1 item (the essays)
    assert len(ds) == 1

    text = ds[0]["text"]

    # Check for upper case as seen in the raw file or standard title
    assert "SELF RELIANCE" in text or "Self-Reliance" in text
    assert "NATURE" in text or "Nature" in text
    assert "COMPENSATION" in text or "Compensation" in text

    print("Ralph Waldo Emerson test passed!")

if __name__ == "__main__":
    test_ralph_waldo_emerson()
