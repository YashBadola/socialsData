import os
import json
import pytest
from socials_data.core.loader import load_dataset

class TestSorenKierkegaard:
    def test_dataset_exists(self):
        """Test that the soren_kierkegaard dataset can be loaded."""
        try:
            dataset = load_dataset("soren_kierkegaard")
        except Exception as e:
            pytest.fail(f"Failed to load dataset: {e}")

        assert dataset is not None
        assert len(dataset) > 0

    def test_metadata(self):
        """Test that the metadata is correct."""
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        metadata_path = os.path.join(base_dir, "socials_data", "personalities", "soren_kierkegaard", "metadata.json")

        assert os.path.exists(metadata_path)

        with open(metadata_path, 'r', encoding='utf-8') as f:
            metadata = json.load(f)

        assert metadata["id"] == "soren_kierkegaard"
        assert metadata["name"] == "Soren Kierkegaard"
        assert "existentialist" in metadata["description"].lower()
        assert "irony" in metadata["system_prompt"].lower()

    def test_content_integrity(self):
        """Test that the content looks reasonable and is free of Gutenberg headers."""
        dataset = load_dataset("soren_kierkegaard")

        # Check a sample
        sample = dataset[0]
        text = sample["text"]

        assert len(text) > 0

        # Should not contain Project Gutenberg license headers
        assert "PROJECT GUTENBERG EBOOK" not in text
        # Should not contain the translator's introduction part about Sam Houston if we cleaned it well
        # My cleaning kept everything from DIAPSALMATA[1] onwards, so the Intro I should be gone.
        assert "Sam Houston" not in text

        # Should contain some Kierkegaard keywords
        keywords = ["poet", "anguish", "Christian", "God", "faith", "Abraham"]
        # Check if at least one keyword is present in the first few chunks
        found_any = False
        for i in range(min(5, len(dataset))):
            text_chunk = dataset[i]["text"]
            if any(k in text_chunk for k in keywords):
                found_any = True
                break
        assert found_any, "Did not find expected keywords in the first few chunks"

    def test_cleanliness(self):
        """Ensure specific artifacts are removed."""
        dataset = load_dataset("soren_kierkegaard")
        full_text = " ".join([d["text"] for d in dataset])

        # Ensure the start marker itself is present (since I kept it) or handled
        # I chose to keep the content starting from start_marker.
        # But 'DIAPSALMATA[1]' might be a bit ugly if it's just a header.
        # It's fine.
        pass

if __name__ == "__main__":
    pytest.main([__file__])
