from socials_data.core.loader import load_dataset

def test_ludwig_wittgenstein_load():
    """
    Test that the Ludwig Wittgenstein dataset can be loaded and contains expected data.
    """
    dataset = load_dataset("ludwig_wittgenstein")

    assert len(dataset) > 0

    # Check if we have entries from both sources
    sources = set(item['source'] for item in dataset)
    assert "tractatus.txt" in sources
    assert "investigations.txt" in sources

    # Check content of a known entry
    tractatus_entry = next(item for item in dataset if item['source'] == "tractatus.txt")
    assert "1 The world is everything that is the case." in tractatus_entry['text']
    assert "7 Whereof one cannot speak, thereof one must be silent." in tractatus_entry['text']
