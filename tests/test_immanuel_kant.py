
import pytest
import os
from socials_data.core.loader import load_dataset, PERSONALITIES_DIR

def test_immanuel_kant_data_integrity():
    """
    Verifies that the Immanuel Kant dataset is correctly loaded and contains valid text.
    """
    dataset = load_dataset("immanuel_kant")

    assert len(dataset) > 0, "Dataset should not be empty"

    sample = dataset[0]
    assert "text" in sample, "Sample should contain 'text'"
    assert "source" in sample, "Sample should contain 'source'"

    # Verify content relevance
    text = sample["text"]
    assert isinstance(text, str)
    assert len(text) > 0

    # Check for keywords specific to Kant's work (checking the whole dataset would be better,
    # but let's check if *some* entry contains these keywords to be robust)

    keywords = ["reason", "critique", "metaphysics", "transcendental", "priori", "pure"]

    # We iterate through a few samples to find keywords
    found_keywords = set()
    for i in range(min(len(dataset), 100)):
        entry_text = dataset[i]["text"].lower()
        for kw in keywords:
            if kw in entry_text:
                found_keywords.add(kw)

    assert len(found_keywords) > 0, f"Should find some Kantian keywords in the first 100 samples. Found: {found_keywords}"

def test_immanuel_kant_metadata():
    """
    Verifies that the metadata file exists and contains correct information.
    """
    import json

    metadata_path = PERSONALITIES_DIR / "immanuel_kant" / "metadata.json"
    assert metadata_path.exists()

    with open(metadata_path, "r") as f:
        metadata = json.load(f)

    assert metadata["id"] == "immanuel_kant"
    assert metadata["name"] == "Immanuel Kant"
    assert "Critique of Pure Reason" in metadata["sources"][0]["title"]
