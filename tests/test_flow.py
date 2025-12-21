from socials_data import load_dataset
import pytest

def test_workflow():
    # Verify we can load the data we just created
    ds_land = load_dataset("nick_land")
    # We added new content, so now there should be 5 items (4 original + 1 added)
    assert len(ds_land) == 5
    # Note: dataset order might vary depending on file system or processing order.
    # We'll check if content exists in any of the items.
    all_text_land = " ".join([item["text"] for item in ds_land])
    assert "Fanged Noumena" in all_text_land
    assert "Neo-China arrives from the future" in all_text_land
    assert "Meltdown: planetary china-syndrome" in all_text_land

    ds_zizek = load_dataset("slavoj_zizek")
    # We added new content, so now there should be 5 items (4 original + 1 added)
    assert len(ds_zizek) == 5
    all_text_zizek = " ".join([item["text"] for item in ds_zizek])
    assert "Ideology" in all_text_zizek
    assert "start eating that trashcan" in all_text_zizek
    assert "Human Rights" in all_text_zizek
    assert "Today, everybody is talking about virtual reality" in all_text_zizek

    ds_aurelius = load_dataset("marcus_aurelius")
    # We added new content, so now there should be 3 items (2 original + 1 added)
    assert len(ds_aurelius) == 3
    all_text_aurelius = " ".join([item["text"] for item in ds_aurelius])
    assert "Of my grandfather Verus" in all_text_aurelius

    ds_seneca = load_dataset("seneca")
    # We added new content, there should be 1 item
    assert len(ds_seneca) == 1
    all_text_seneca = " ".join([item["text"] for item in ds_seneca])
    assert "Greetings from Seneca to his friend Lucilius" in all_text_seneca
    assert "Nothing, Lucilius, is ours, except time" in all_text_seneca

    print("Workflow test passed!")

if __name__ == "__main__":
    test_workflow()
