from socials_data import load_dataset
import pytest

def test_simone_de_beauvoir_loading():
    # Verify we can load the data for Simone de Beauvoir
    ds = load_dataset("simone_de_beauvoir")

    # We should have 8 items (Title + 7 paragraphs)
    assert len(ds) == 8

    # Check content
    all_text = " ".join([item["text"] for item in ds])

    assert "The human condition is one of fundamental ambiguity" in all_text
    assert "Freedom is not a given; it is a conquest" in all_text
    assert "One cannot will oneself free without willing others free" in all_text
    assert "One is not born, but rather becomes, a woman" in all_text

    # Check source field
    assert ds[0]["source"] == "Reflections on Ambiguity and Existence"

if __name__ == "__main__":
    test_simone_de_beauvoir_loading()
