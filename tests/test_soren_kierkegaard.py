from socials_data import load_dataset

def test_soren_kierkegaard():
    ds = load_dataset("soren_kierkegaard")
    # We added 2 items
    assert len(ds) == 2

    all_text = " ".join([item["text"] for item in ds])
    assert "Knight of Faith" in all_text
    assert "sickness unto death" in all_text
    print("Søren Kierkegaard test passed!")

if __name__ == "__main__":
    test_soren_kierkegaard()
