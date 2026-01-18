import pytest
from socials_data.core.loader import load_dataset

def test_load_bertrand_russell_dataset():
    """Test that the Bertrand Russell dataset can be loaded and contains valid data."""
    dataset = load_dataset("bertrand_russell")

    # Check if dataset is not empty
    assert len(dataset) > 0, "Dataset should not be empty"
    # We expect 4 items as we processed 4 files and the processor creates 1 item per file
    assert len(dataset) == 4, f"Expected 4 items, got {len(dataset)}"

    # Check sources
    sources = set(item["source"] for item in dataset)
    expected_sources = {
        "The_Problems_of_Philosophy.txt",
        "Political_Ideals.txt",
        "Mysticism_and_Logic.txt",
        "Proposed_Roads_to_Freedom.txt"
    }

    assert sources == expected_sources, f"Sources mismatch. Found: {sources}, Expected: {expected_sources}"

    # Verify content for each file
    for item in dataset:
        text = item["text"]
        source = item["source"]
        assert len(text) > 100, f"Text content for {source} is too short."

        if source == "The_Problems_of_Philosophy.txt":
            assert "philosophy" in text.lower()
            assert "appearance" in text.lower() or "knowledge" in text.lower()
        elif source == "Political_Ideals.txt":
            assert "political" in text.lower()
            assert "ideals" in text.lower() or "capitalism" in text.lower()
        elif source == "Mysticism_and_Logic.txt":
            assert "mysticism" in text.lower()
            assert "logic" in text.lower()
        elif source == "Proposed_Roads_to_Freedom.txt":
            assert "freedom" in text.lower()
            assert "anarchism" in text.lower() or "socialism" in text.lower()

if __name__ == "__main__":
    test_load_bertrand_russell_dataset()
