from socials_data.core.loader import load_dataset
import pytest

def test_load_dataset():
    # Load the processed dataset for Simone de Beauvoir
    try:
        ds = load_dataset("simone_de_beauvoir")
    except Exception as e:
        pytest.fail(f"Failed to load dataset: {e}")

    # Check if the dataset is not empty
    assert len(ds) >= 1

    # Check the first item structure
    item = ds[0]
    assert "text" in item
    assert isinstance(item["text"], str)
    assert len(item["text"]) > 0
    assert "source" in item
    assert isinstance(item["source"], str)

    # Verify content snippets from our added files are present in the dataset
    texts = [row["text"] for row in ds]

    # Check for "The Second Sex" content
    assert any("For a long time I have hesitated to write a book on woman." in text for text in texts)

    # Check for "The Ethics of Ambiguity" content
    assert any("The man who finds himself cast into a world which he has not helped to establish" in text for text in texts)

    # Check for "Memoirs" content
    assert any("I was born at four o'clock in the morning on the 9th of January 1908" in text for text in texts)
