import os
import pytest
from socials_data import load_dataset
from socials_data.core.manager import PersonalityManager

def test_john_locke_dataset():
    # 1. Check metadata
    manager = PersonalityManager()
    metadata = manager.get_metadata("john_locke")
    assert metadata["name"] == "John Locke"
    assert len(metadata["sources"]) == 3

    # 2. Check files exist
    base_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "../socials_data/personalities/john_locke")
    assert os.path.exists(os.path.join(base_dir, "raw/second_treatise_of_government.txt"))
    assert os.path.exists(os.path.join(base_dir, "processed/data.jsonl"))

    # 3. Load dataset
    ds = load_dataset("john_locke")

    # Verify it's a Dataset object (has features, num_rows, etc)
    assert hasattr(ds, "features")
    assert len(ds) > 0

    # 4. Check content
    # We should find some Locke keywords in the text
    # Since dataset is just a list of chunks (or one big chunk if not split), we check the first one.
    text_sample = ds[0]["text"]
    assert "Government" in text_sample or "Understanding" in text_sample or "Idea" in text_sample
    assert isinstance(text_sample, str)
    assert len(text_sample) > 100

if __name__ == "__main__":
    pytest.main([__file__])
