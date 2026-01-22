from socials_data import load_dataset
import pytest

def test_soren_kierkegaard_dataset():
    """Test that the Soren Kierkegaard dataset loads correctly."""
    dataset = load_dataset("soren_kierkegaard")

    # Check that we have data
    assert len(dataset) > 0

    # Check the fields
    assert "text" in dataset[0]

    # Verify content snippet (optional)
    text_content = [item["text"] for item in dataset]
    assert any("The crowd is untruth" in text for text in text_content)
    assert any("Anxiety is the dizziness of freedom" in text for text in text_content)
