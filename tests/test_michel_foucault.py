from socials_data import load_dataset

def test_michel_foucault_content():
    ds = load_dataset("michel_foucault")
    assert len(ds) > 0

    found_panopticon = False
    found_discipline = False

    for item in ds:
        text = item['text']
        if "Panopticon" in text:
            found_panopticon = True
        if "Means of Correct Training" in text:
            found_discipline = True

    assert found_panopticon, "Panopticon content not found"
    assert found_discipline, "Discipline content not found"
