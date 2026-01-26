from socials_data.core.loader import load_dataset

def test_michel_foucault_dataset():
    dataset = load_dataset("michel_foucault")
    assert len(dataset) >= 1
    text = dataset[0]["text"]
    assert "plague" in text
    assert "panopticism" in text.lower() or "surveillance" in text.lower()
