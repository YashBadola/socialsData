import pytest
import os
import json
from pathlib import Path
from socials_data.core.manager import PersonalityManager
from socials_data.core.processor import TextDataProcessor

class TestPlato:
    def test_plato_dataset_creation(self):
        """
        Verify that Plato's dataset can be processed and contains expected content.
        """
        # Ensure we are in the root
        manager = PersonalityManager()
        personality_id = "plato"

        # Verify metadata
        meta = manager.get_metadata(personality_id)
        assert meta["name"] == "Plato"
        assert meta["id"] == "plato"
        assert "Socrates" in meta["system_prompt"]

        # Verify processed data exists
        processed_file = manager.base_dir / personality_id / "processed" / "data.jsonl"
        assert processed_file.exists()
        assert processed_file.stat().st_size > 0

        # Read and verify content
        found_apology = False
        found_republic = False
        found_keyword = False

        with open(processed_file, "r", encoding="utf-8") as f:
            for line in f:
                record = json.loads(line)
                text = record["text"]
                source = record["source"]

                # Check for sources
                if "apology.txt" in source:
                    found_apology = True
                if "republic.txt" in source:
                    found_republic = True

                # Check for content keywords (Gutenberg headers should be stripped)
                # "Project Gutenberg" might still be in the preamble if not caught by my simple logic,
                # but let's check if the text *starts* with relevant content or contains it.
                if "Socrates" in text or "justice" in text:
                    found_keyword = True

                # Check that strict header is gone (if my stripper worked)
                # Note: My stripper looks for *** START OF ...
                # It keeps the text between START and END.
                # Gutenberg texts often have legal mumbo jumbo at the start.
                # If my code worked, it should be gone.
                assert "*** START OF THE PROJECT GUTENBERG EBOOK" not in text

        assert found_apology, "Apology text not found in processed data"
        assert found_republic, "Republic text not found in processed data"
        assert found_keyword, "Expected keywords not found"

    def test_gutenberg_cleaning(self):
        """
        Test the Gutenberg cleaning logic specifically.
        """
        processor = TextDataProcessor()

        raw_text = """
The Project Gutenberg eBook of The Republic
This is a preamble.

*** START OF THE PROJECT GUTENBERG EBOOK THE REPUBLIC ***

Book I

Socrates: I went down yesterday to the Piraeus...

*** END OF THE PROJECT GUTENBERG EBOOK THE REPUBLIC ***

End of text info.
        """

        cleaned = processor._clean_gutenberg_text(raw_text)
        assert "Book I" in cleaned
        assert "Socrates: I went down" in cleaned
        assert "preamble" not in cleaned
        assert "End of text info" not in cleaned
        assert "*** START" not in cleaned
