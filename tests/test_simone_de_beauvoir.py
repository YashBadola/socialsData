from socials_data import load_dataset
import pytest

def test_simone_de_beauvoir_dataset():
    # Verify we can load the data for Simone de Beauvoir
    ds = load_dataset("simone_de_beauvoir")

    # We added 3 items
    assert len(ds) == 3

    # Check content
    all_text = " ".join([item["text"] for item in ds])

    # Check for key phrases from our simulated files
    assert "One is not born, but rather becomes, a woman" in all_text
    assert "My Dear Sartre" in all_text
    assert "The continuous work of our life is to build death" in all_text

    # Check sources
    sources = [item["source"] for item in ds]
    assert "the_second_sex_excerpt.txt" in sources
    assert "letter_to_sartre.txt" in sources
    assert "ethics_of_ambiguity_excerpt.txt" in sources

if __name__ == "__main__":
    test_simone_de_beauvoir_dataset()
