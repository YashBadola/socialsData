
def test_plato_dataset():
    from socials_data import load_dataset
    dataset = load_dataset("plato")
    assert len(dataset) > 0
    assert "text" in dataset[0]
    assert isinstance(dataset[0]["text"], str)
    assert len(dataset[0]["text"]) > 0
