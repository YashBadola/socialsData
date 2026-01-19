import os
import json
from socials_data import load_dataset

def test_voltaire_structure():
    base_path = "socials_data/personalities/voltaire"
    assert os.path.exists(base_path)
    assert os.path.exists(os.path.join(base_path, "metadata.json"))
    assert os.path.exists(os.path.join(base_path, "raw"))
    assert os.path.exists(os.path.join(base_path, "processed"))

    with open(os.path.join(base_path, "metadata.json"), "r") as f:
        metadata = json.load(f)
        assert metadata["id"] == "voltaire"
        assert metadata["name"] == "Voltaire"
        assert "system_prompt" in metadata
        assert len(metadata["sources"]) == 3

def test_voltaire_dataset_load():
    # Test loading the dataset using the library function
    dataset = load_dataset("voltaire")
    assert dataset is not None
    assert len(dataset) >= 3

    # Check content of one of the items
    texts = [item['text'] for item in dataset]
    assert any("FANATICISM" in text for text in texts)
    assert any("Thunder-ten-tronckh" in text for text in texts)
    assert any("ON TRADE" in text for text in texts)
