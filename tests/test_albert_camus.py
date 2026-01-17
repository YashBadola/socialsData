from socials_data import load_dataset
import pytest

def test_albert_camus_loading():
    # Verify we can load the data for Albert Camus
    ds_camus = load_dataset("albert_camus")

    # We should have at least 1 item since we added one raw file
    assert len(ds_camus) >= 1

    # Check if the content contains some of the text we added
    all_text_camus = " ".join([item["text"] for item in ds_camus])

    assert "Sisyphus" in all_text_camus
    assert "The absurd is born" in all_text_camus
    assert "invincible summer" in all_text_camus

    print("Albert Camus dataset loaded successfully!")

if __name__ == "__main__":
    test_albert_camus_loading()
