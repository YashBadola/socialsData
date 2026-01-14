from socials_data import load_dataset
import pytest

def test_vitruvius():
    ds = load_dataset("vitruvius")
    assert len(ds) > 0
    # Join all text to search for keywords
    all_text = " ".join([item["text"] for item in ds])

    # Check for the three principles (which are in the text I added)
    # Actually, "Firmitas" etc might be in the QA, but here we are loading 'data.jsonl'
    # which contains the raw text chunks.
    # In my raw text, I have "Firmitas", "Utilitas", "Venustas" mentioned?
    # Let's check the raw text I wrote.
    # I wrote: "Architecture depends on Order... Eurythmy, Symmetry, Propriety, and Economy"
    # Wait, the famous triad "Firmitas, Utilitas, Venustas" is in Book I Chapter III.
    # "All these must be built with due reference to durability, convenience, and beauty."
    # The Latin terms might not be in the translation I used?
    # I used Morgan's translation excerpts.
    # In Chapter III paragraph 2: "durability, convenience, and beauty."

    assert "durability" in all_text
    assert "convenience" in all_text
    assert "beauty" in all_text
    assert "Vitruvius" in all_text or "Architect" in all_text

    print("Vitruvius test passed!")

if __name__ == "__main__":
    test_vitruvius()
