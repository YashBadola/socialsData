from socials_data import load_dataset

def test_seneca_dataset_structure():
    dataset = load_dataset('seneca')
    assert dataset is not None
    assert len(dataset) > 0
    sample = dataset[0]
    assert 'text' in sample
    assert isinstance(sample['text'], str)
    assert len(sample['text']) > 0
