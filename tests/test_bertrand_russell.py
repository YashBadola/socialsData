import os
import pytest
from socials_data.core.loader import load_dataset

def test_load_bertrand_russell_dataset():
    """Test that the Bertrand Russell dataset can be loaded and contains valid data."""
    dataset = load_dataset("bertrand_russell")

    # Check if dataset is not empty
    assert len(dataset) == 4, f"Dataset should contain exactly 4 documents, found {len(dataset)}"

    expected_sources = {
        "problems_of_philosophy.txt",
        "analysis_of_mind.txt",
        "mysticism_and_logic.txt",
        "proposed_roads_to_freedom.txt"
    }

    found_sources = set()

    # Specific keywords we expect in Russell's text
    # General philosophy keywords + title specific
    keywords_map = {
        "problems_of_philosophy.txt": ["philosophy", "knowledge", "appearance", "reality"],
        "analysis_of_mind.txt": ["mind", "consciousness", "psychology", "sensation"],
        "mysticism_and_logic.txt": ["mysticism", "logic", "scientific", "method"],
        "proposed_roads_to_freedom.txt": ["socialism", "anarchism", "syndicalism", "freedom"]
    }

    for item in dataset:
        assert "text" in item, "Item should contain 'text' field"
        assert "source" in item, "Item should contain 'source' field"

        source = item["source"]
        found_sources.add(source)

        text = item["text"]
        assert isinstance(text, str), "Text should be a string"
        assert len(text) > 1000, f"Text in {source} seems too short ({len(text)} chars)"

        # Check specific keywords for the source
        if source in keywords_map:
            expected_keys = keywords_map[source]
            found_any = False
            for k in expected_keys:
                if k.lower() in text.lower():
                    found_any = True
                    break
            assert found_any, f"Did not find any expected keywords {expected_keys} in {source}"

    assert found_sources == expected_sources, f"Sources mismatch. Expected {expected_sources}, found {found_sources}"

if __name__ == "__main__":
    test_load_bertrand_russell_dataset()
