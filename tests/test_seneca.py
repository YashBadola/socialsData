from socials_data import load_dataset
import pytest

def test_seneca_workflow():
    # Verify we can load the data we just created
    ds_seneca = load_dataset("seneca")

    # We added 2 files, so there should be 2 items
    assert len(ds_seneca) == 2

    all_text_seneca = " ".join([item["text"] for item in ds_seneca])

    # Check for text from "On the Shortness of Life"
    assert "It is not that we have a short time to live" in all_text_seneca
    assert "Life is long enough" in all_text_seneca

    # Check for text from "Letters to Lucilius"
    assert "Continue to act thus, my dear Lucilius" in all_text_seneca
    assert "The most disgraceful kind of loss, however, is that due to carelessness" in all_text_seneca

    print("Seneca workflow test passed!")
