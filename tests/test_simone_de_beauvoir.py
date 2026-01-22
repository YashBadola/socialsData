
import pytest
from socials_data.core.loader import load_dataset
from socials_data.core.manager import PersonalityManager

def test_simone_de_beauvoir_structure():
    """Check that Simone de Beauvoir exists and has the correct structure."""
    manager = PersonalityManager()
    personalities = manager.list_personalities()
    assert "simone_de_beauvoir" in personalities

    metadata = manager.get_metadata("simone_de_beauvoir")
    assert metadata["name"] == "Simone de Beauvoir"
    assert metadata["id"] == "simone_de_beauvoir"
    assert "The Ethics of Ambiguity" in [s["title"] for s in metadata["sources"]]

def test_load_dataset():
    """Check that we can load the processed dataset."""
    ds = load_dataset("simone_de_beauvoir")
    assert len(ds) > 0

    # Check if the text content makes sense (contains keywords)
    # Since we used a synthetic text, we know what to look for.
    text_content = ""
    for item in ds:
        text_content += item["text"]

    assert "Ambiguity" in text_content or "freedom" in text_content
