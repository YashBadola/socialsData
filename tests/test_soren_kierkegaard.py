
import pytest
from socials_data.core.loader import load_dataset

def test_soren_kierkegaard_dataset_loading():
    """Test that the Søren Kierkegaard dataset can be loaded."""
    dataset = load_dataset("soren_kierkegaard")
    assert len(dataset) > 0
    assert "text" in dataset[0]

    # Check if we can find some characteristic text
    texts = [item['text'] for item in dataset]
    assert any("Fear and Trembling" in text or "Abraham" in text for text in texts)
    assert any("The Despair that is Conscious of being Despair" in text for text in texts)
    assert any("The Aesthetic Validity of Marriage" in text for text in texts)
