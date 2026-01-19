from socials_data import load_dataset

def test_seneca():
    # Verify we can load the data we just created
    ds = load_dataset("seneca")

    # We added 2 files, so we expect 2 records
    assert len(ds) == 2

    all_text = " ".join([item["text"] for item in ds])

    # Check for content from letters.txt
    assert "Greetings from Seneca to his friend Lucilius" in all_text
    assert "Everywhere means nowhere" in all_text

    # Check for content from on_shortness_of_life.txt
    assert "It is not that we have a short time to live" in all_text
    assert "You act like mortals in all that you fear" in all_text

    print("Seneca test passed!")

if __name__ == "__main__":
    test_seneca()
