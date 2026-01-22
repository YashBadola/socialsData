from socials_data.core.loader import load_dataset
import pytest

def test_voltaire_dataset_loads():
    ds = load_dataset("voltaire")
    assert len(ds) > 0
    assert "text" in ds[0]

def test_voltaire_content():
    ds = load_dataset("voltaire")
    texts = [row["text"] for row in ds]

    # Check for Candide
    assert any("CANDIDE" in text for text in texts)
    assert any("Pangloss" in text for text in texts)

    # Check for Letters on England
    assert any("LETTER VIII" in text for text in texts)
    assert any("The Members of the English Parliament" in text for text in texts)

    # Check for Philosophical Dictionary
    assert any("LIBERTY" in text for text in texts)
    assert any("Either I am mistaken, or liberty is only the power of acting" in text for text in texts)
