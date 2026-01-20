from socials_data.core.loader import load_dataset
import pytest

def test_load_dataset_simone_de_beauvoir():
    dataset = load_dataset("simone_de_beauvoir")
    assert dataset is not None
    assert len(dataset) > 0

    # Check if the content resembles what we added
    texts = [item['text'] for item in dataset]
    sources = [item['source'] for item in dataset]

    # Use any to check if at least one entry matches the source file names
    assert any("the_second_sex_intro.txt" in source for source in sources)
    assert any("memoirs_excerpt.txt" in source for source in sources)
    assert any("ethics_of_ambiguity_excerpt.txt" in source for source in sources)

if __name__ == "__main__":
    test_load_dataset_simone_de_beauvoir()
