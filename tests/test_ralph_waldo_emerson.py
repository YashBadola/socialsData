import os
import pytest
from socials_data import load_dataset
from socials_data.core.manager import PersonalityManager

def test_ralph_waldo_emerson_dataset():
    personality_id = "ralph_waldo_emerson"

    # 1. Verify Manager can find it
    manager = PersonalityManager()
    metadata = manager.get_metadata(personality_id)
    assert metadata["id"] == personality_id
    assert metadata["name"] == "Ralph Waldo Emerson"
    assert len(metadata["sources"]) == 3

    # 2. Verify dataset loads
    ds = load_dataset(personality_id)
    assert len(ds) > 0

    # 3. Check content
    # Since load_dataset returns a Hugging Face Dataset, slicing returns a dict of lists
    sample_text = ds[0]["text"]
    assert isinstance(sample_text, str)
    assert len(sample_text) > 0

    # 4. Check for key terms
    # We expect terms like "nature", "soul", "self-reliance" to appear somewhere in the dataset
    found_term = False
    for i in range(min(len(ds), 100)):
        text = ds[i]["text"].lower()
        if "nature" in text or "soul" in text or "self" in text:
            found_term = True
            break
    assert found_term, "Did not find expected terms in the first 100 chunks"

    # 5. Check sources
    sources = set(ds["source"])
    assert "essays_first_series.txt" in sources
    assert "essays_second_series.txt" in sources
    assert "nature.txt" in sources
