from socials_data import load_dataset
import pytest

def test_seneca_load():
    ds = load_dataset("seneca")
    assert len(ds) == 3
    all_text = " ".join([item["text"] for item in ds])
    assert "Greetings from Seneca to his friend Lucilius" in all_text
    assert "Reason is strong only so long as it stands aloof from the passions" in all_text
    assert "DO you ask me what you should regard as especially to be avoided?" in all_text

if __name__ == "__main__":
    test_seneca_load()
