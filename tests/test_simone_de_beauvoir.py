from socials_data import load_dataset
import pytest

def test_simone_de_beauvoir():
    # Verify we can load the data for Simone de Beauvoir
    ds = load_dataset("simone_de_beauvoir")
    assert len(ds) == 2

    all_text = " ".join([item["text"] for item in ds])
    assert "One is not born, but rather becomes, a woman" in all_text
    assert "The Ethics of Ambiguity" in all_text.title() or "THE ETHICS OF AMBIGUITY" in all_text

if __name__ == "__main__":
    test_simone_de_beauvoir()
