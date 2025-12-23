import os
import pytest
from socials_data.core.loader import load_dataset
from socials_data.core.manager import PersonalityManager

class TestPlato:
    def test_metadata_exists(self):
        manager = PersonalityManager()
        metadata = manager.get_metadata("plato")
        assert metadata["name"] == "Plato"
        assert metadata["id"] == "plato"
        assert len(metadata["sources"]) == 3

    def test_load_dataset(self):
        # Test loading the processed dataset
        dataset = load_dataset("plato")
        assert dataset is not None
        assert len(dataset) > 0

        # Verify columns
        assert "text" in dataset.column_names
        assert "source" in dataset.column_names

    def test_content_relevance(self):
        dataset = load_dataset("plato")

        # Check for keywords in a sample of texts
        keywords = ["Socrates", "justice", "virtue", "truth", "dialogue", "Apology", "Republic", "Symposium"]
        found_keywords = set()

        # Check first 100 entries or all if less
        sample_size = min(len(dataset), 100)
        for i in range(sample_size):
            text = dataset[i]["text"]
            for keyword in keywords:
                if keyword in text:
                    found_keywords.add(keyword)

        # We expect at least some of these keywords to be found
        assert len(found_keywords) > 0, "No relevant keywords found in the dataset sample"

        # Specifically look for Socrates since he's central
        socrates_found = any("Socrates" in dataset[i]["text"] for i in range(sample_size))
        assert socrates_found, "Socrates not found in the dataset sample"

    def test_source_attribution(self):
        dataset = load_dataset("plato")
        sources = set(dataset["source"])
        expected_sources = {"the_republic.txt", "apology.txt", "symposium.txt"}

        # Check that we have at least one of the expected sources
        assert not sources.isdisjoint(expected_sources)
