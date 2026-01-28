from socials_data import load_dataset

def test_load_camus():
    dataset = load_dataset("albert_camus")
    assert len(dataset) > 0
    assert "Sisyphus" in dataset[0]['text']
