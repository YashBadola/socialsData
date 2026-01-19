from socials_data import load_dataset
import pytest

def test_simone_de_beauvoir():
    # Verify we can load the data for Simone de Beauvoir
    ds = load_dataset("simone_de_beauvoir")

    # We added 4 files, so we expect at least 4 items.
    assert len(ds) >= 4

    all_text = " ".join([item["text"] for item in ds])

    # Check for content from "The Second Sex"
    assert "One is not born, but rather becomes, a woman" in all_text

    # Check for content from "The Ethics of Ambiguity"
    assert "The continuous work of our life, says Montaigne, is to build death" in all_text

    # Check for content from "Childhood"
    assert "The category of the Other is as primordial as consciousness itself" in all_text

    # Check for quotes
    assert "Change your life today. Don't gamble on the future, act now, without delay" in all_text

    print("Simone de Beauvoir test passed!")
