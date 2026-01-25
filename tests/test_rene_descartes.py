from socials_data import load_dataset

def test_rene_descartes_dataset():
    dataset = load_dataset("rene_descartes")
    assert len(dataset) > 0

    text = " ".join([item["text"] for item in dataset])

    # Check for phrases from Discourse on the Method
    assert "COGITO ERGO SUM" in text
    assert "Good sense is, of all things among men, the most equally distributed" in text

    # Check for phrases from Meditations
    assert "_Archimedes_ required but a _point_ which was _firm_" in text
    assert "I am a _Thinking Thing_" in text

if __name__ == "__main__":
    test_rene_descartes_dataset()
