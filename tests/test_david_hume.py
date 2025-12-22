import pytest
import os
from socials_data.core.loader import load_dataset

PERSONALITY_ID = "david_hume"

def test_load_dataset():
    dataset = load_dataset(PERSONALITY_ID)
    assert len(dataset) > 0

    # Check a sample
    sample = dataset[0]
    assert "text" in sample
    assert "source" in sample
    assert isinstance(sample["text"], str)
    assert len(sample["text"]) > 0

    # Verify content relevance
    # We expect words like "reason", "passion", "impression", "idea", "skepticism"
    # But since we have random chunks, we just check if any of the chunks contain common words.

    keywords = ["reason", "passion", "impression", "idea", "nature", "understanding", "cause", "effect"]

    found_keyword = False
    for i in range(min(len(dataset), 100)):
        text = dataset[i]["text"].lower()
        if any(k in text for k in keywords):
            found_keyword = True
            break

    assert found_keyword, f"Could not find any of {keywords} in the first 100 samples."
