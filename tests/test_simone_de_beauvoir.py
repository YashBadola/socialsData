from socials_data import load_dataset
import pytest

def test_simone_de_beauvoir_data():
    # Verify we can load the data for Simone de Beauvoir
    ds = load_dataset("simone_de_beauvoir")

    # We added 3 files, so there should be 3 items
    assert len(ds) == 3

    all_text = " ".join([item["text"] for item in ds])

    # Check for text from The Second Sex
    assert "One is not born, but rather becomes, a woman." in all_text
    assert "He is the Subject, he is the Absolute - she is the Other." in all_text

    # Check for text from The Ethics of Ambiguity
    assert "The word \"ambiguity\" is not a label I chose lightly." in all_text
    assert "To exist is to be a continuous disclosure of the world." in all_text
    assert "We are condemned to be free." in all_text

    # Check for text from Memoirs
    assert "I was born at four o'clock in the morning on the 9th of January 1908" in all_text
    assert "I met Jean-Paul Sartre at the Sorbonne." in all_text
