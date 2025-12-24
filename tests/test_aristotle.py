import os
import json
import pytest
from socials_data.core.loader import load_dataset

class TestAristotle:
    @property
    def personality_id(self):
        return "aristotle"

    def test_dataset_loads(self):
        """Test that the dataset can be loaded using the library function."""
        dataset = load_dataset(self.personality_id)
        assert len(dataset) > 0, "Dataset should not be empty"
        assert "text" in dataset.features, "Dataset should have a 'text' column"
        assert "source" in dataset.features, "Dataset should have a 'source' column"

    def test_content_verification(self):
        """Test that the content contains expected strings from Aristotle's works."""
        dataset = load_dataset(self.personality_id)

        # Check for presence of each book by filename in source
        sources = set(dataset["source"])
        expected_sources = {
            "nicomachean_ethics.txt",
            "politics.txt",
            "poetics.txt",
            "categories.txt"
        }

        missing = expected_sources - sources
        assert not missing, f"Missing sources: {missing}"

        # Check for specific famous lines or terms
        # Note: Dataset is chunked, so we need to search through samples.
        # Efficiently sample or search.

        keywords = {
            "nicomachean_ethics.txt": ["virtue", "happiness", "mean"],
            "politics.txt": ["state", "citizen", "government"],
            "poetics.txt": ["tragedy", "imitation", "plot"],
            "categories.txt": ["substance", "quality", "quantity"]
        }

        found_keywords = {k: False for k in keywords}

        # Check a sample of the data to avoid O(N) scan if N is huge, but N is small here (~20k lines max)
        for row in dataset:
            src = row["source"]
            text = row["text"].lower()

            if src in keywords:
                for kw in keywords[src]:
                    if kw in text:
                        # We can't easily mark specific keyword as found per file in a single dict without nesting
                        # But simpler: just ensure we find *some* keywords for *each* file eventually.
                        pass

        # Let's do a more targeted check.
        # Verify that for each source, we can find at least one of its keywords in the dataset

        for src, kws in keywords.items():
            src_rows = dataset.filter(lambda x: x["source"] == src)
            assert len(src_rows) > 0, f"No data for {src}"

            # Check if any row contains any keyword
            has_keyword = False
            for row in src_rows:
                if any(kw in row["text"].lower() for kw in kws):
                    has_keyword = True
                    break
            assert has_keyword, f"No keywords {kws} found in {src}"

    def test_metadata(self):
        """Verify metadata.json exists and is valid."""
        base_dir = os.path.dirname(os.path.abspath(__file__))
        # Go up one level from tests/ to root, then to personality
        meta_path = os.path.join(base_dir, "..", "socials_data", "personalities", self.personality_id, "metadata.json")

        assert os.path.exists(meta_path)

        with open(meta_path, "r") as f:
            data = json.load(f)

        assert data["id"] == self.personality_id
        assert "system_prompt" in data
        assert len(data["sources"]) == 4
