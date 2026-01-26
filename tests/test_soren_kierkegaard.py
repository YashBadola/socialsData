from socials_data import load_dataset
import pytest

def test_soren_kierkegaard():
    dataset = load_dataset("soren_kierkegaard")

    # Check if we have the 5 expected works
    # Note: load_dataset returns a list of dictionaries, one for each "chunk" (line in jsonl)
    # Since we processed each file as one chunk (TextDataProcessor behavior for small files or as implemented),
    # we should have 5 records if the splitting script worked as expected and processor read them.
    # Actually, TextDataProcessor reads each file in raw/ and outputs one record per file.
    assert len(dataset) == 5

    # Combine all text to search
    all_text = " ".join([item["text"] for item in dataset])

    # Check for titles/phrases
    assert "DIAPSALMATA" in all_text
    assert "IN VINO VERITAS" in all_text
    assert "FEAR AND TREMBLING" in all_text
    assert "PREPARATION FOR A CHRISTIAN LIFE" in all_text
    assert "THE PRESENT MOMENT" in all_text

    # Check for specific content
    assert "What is a poet?" in all_text
    assert "God tempted Abraham" in all_text
    assert "Come hither unto me, all ye that labor" in all_text

if __name__ == "__main__":
    test_soren_kierkegaard()
