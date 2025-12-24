
import os
import pytest
from socials_data.core.loader import load_dataset

def test_jean_jacques_rousseau_dataset():
    # Load dataset
    ds = load_dataset("jean_jacques_rousseau")

    # Check if it returns a Dataset object
    assert hasattr(ds, "features")

    # Check length (we have 3 source files, so at least 3 entries, potentially more if chunked, but standard processor might not chunk)
    assert len(ds) >= 3

    # Check content
    text_content = [item["text"] for item in ds]
    combined_text = " ".join(text_content)

    # Keywords for each book
    assert "social contract" in combined_text.lower() or "man is born free" in combined_text.lower()
    assert "confessions" in combined_text.lower() or "my purpose is to display to my kind a portrait" in combined_text.lower()
    assert "emile" in combined_text.lower() or "god makes all things good" in combined_text.lower()

    # Check source field
    sources = [item["source"] for item in ds]
    assert any("social_contract_and_discourses.txt" in s for s in sources)
    assert any("confessions.txt" in s for s in sources)
    assert any("emile.txt" in s for s in sources)

if __name__ == "__main__":
    test_jean_jacques_rousseau_dataset()
