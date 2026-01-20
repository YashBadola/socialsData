from socials_data import load_dataset
import pytest

def test_load_simone_de_beauvoir():
    """Test that we can load the Simone de Beauvoir dataset."""
    dataset = load_dataset("simone_de_beauvoir")
    assert dataset is not None
    assert len(dataset) > 0

    # Check that we have the expected keys
    sample = dataset[0]
    assert "text" in sample
    assert "source" in sample

    # Check for content from the raw files
    texts = [row["text"] for row in dataset]
    sources = [row["source"] for row in dataset]

    # Verify sources
    assert "the_second_sex_intro.txt" in sources
    assert "ethics_of_ambiguity.txt" in sources
    assert "memoirs.txt" in sources

    # Verify some content
    found_quote = False
    for text in texts:
        if "One is not born, but rather becomes, a woman" in text:
            found_quote = True
            break
    assert found_quote
