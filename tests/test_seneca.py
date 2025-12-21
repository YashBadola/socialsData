import pytest
import os
import json
from socials_data.core.processor import TextDataProcessor

def test_seneca_processing():
    """Test that the Seneca dataset is processed correctly."""

    # Path to the expected processed file
    processed_path = os.path.join("socials_data", "personalities", "seneca", "processed", "data.jsonl")

    # Ensure the file exists
    assert os.path.exists(processed_path), f"Processed data file not found at {processed_path}"

    # Read the file and check basic content
    with open(processed_path, "r", encoding="utf-8") as f:
        line = f.readline()
        assert line, "Processed file is empty"

        data = json.loads(line)
        assert "text" in data, "JSON entry missing 'text' field"
        assert "source" in data, "JSON entry missing 'source' field"

        # Check for some characteristic text (Project Gutenberg License usually at end/start)
        # But we also want to see if it actually contains the content we expect.
        # Since I used "Seneca's Morals", let's look for "Seneca" in the text
        assert "Seneca" in data["text"] or "SENECA" in data["text"], "Text does not appear to contain 'Seneca'"
        assert data["source"] == "seneca_morals.txt", "Source filename mismatch"

if __name__ == "__main__":
    pytest.main([__file__])
