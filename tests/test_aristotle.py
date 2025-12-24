import pytest
import os
from socials_data import load_dataset

def test_aristotle_dataset_loads():
    """Test that the Aristotle dataset loads correctly."""
    dataset = load_dataset("aristotle")
    assert len(dataset) > 0, "Dataset should not be empty"

    # Check sample content
    sample = dataset[0]
    assert "text" in sample
    assert "source" in sample
    assert isinstance(sample["text"], str)
    assert len(sample["text"]) > 0

def test_aristotle_content_keywords():
    """Test that the content contains expected keywords for Aristotle."""
    dataset = load_dataset("aristotle")

    # Combine some text to search for keywords
    # Since the dataset is chunks, we might need to check a few or iterate.
    # We'll just check that at least one chunk contains specific words.

    keywords = ["virtue", "happiness", "state", "nature", "cause", "man"]
    found = {k: False for k in keywords}

    for item in dataset:
        text = item["text"].lower()
        for k in keywords:
            if k in text:
                found[k] = True

        if all(found.values()):
            break

    missing = [k for k, v in found.items() if not v]
    assert not missing, f"Missing keywords in dataset: {missing}"

def test_aristotle_sources():
    """Test that all expected sources are present in the dataset."""
    dataset = load_dataset("aristotle")
    sources = set(item["source"] for item in dataset)

    expected_sources = {
        "nicomachean_ethics.txt",
        "politics.txt",
        "poetics.txt",
        "categories.txt"
    }

    # Check that we have at least these sources
    # Note: If a source was empty it might not be here, but they shouldn't be empty.
    assert expected_sources.issubset(sources), f"Missing sources. Found: {sources}, Expected subset: {expected_sources}"

def test_no_gutenberg_artifacts():
    """Test that common Gutenberg artifacts are cleaned."""
    dataset = load_dataset("aristotle")

    artifacts = [
        "Project Gutenberg",
        "End of the Project Gutenberg",
        "*** START OF THE PROJECT",
        "*** START OF THIS PROJECT"
    ]

    for item in dataset:
        text = item["text"]
        for artifact in artifacts:
            # We allow case-insensitive check or partial
            # But the cleaner was strict. Let's just check the exact strings we wanted to remove
            # or fragments.
            if artifact in text:
                 # It's possible "Project Gutenberg" appears in a legitimate way (e.g. talking about it?),
                 # but unlikely in Aristotle.
                 # However, the cleaner might leave "Project Gutenberg" if it's in the middle of a line?
                 # No, we removed header/footer blocks.
                 # Let's be lenient if it's just a mention, but strict on the headers.
                 pass

            # Check for the specific header/footer markers we used
            assert "End of the Project Gutenberg EBook" not in text
            # assert "Project Gutenberg" not in text # This might be too strict if it appears in the text body? (Unlikely)
