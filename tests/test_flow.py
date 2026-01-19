from socials_data import load_dataset
import pytest

def test_workflow():
    # Verify we can load the data we just created
    ds_land = load_dataset("nick_land")
    # We added new content, so now there should be 6 items (4 original + 2 added)
    assert len(ds_land) == 6
    # Note: dataset order might vary depending on file system or processing order.
    # We'll check if content exists in any of the items.
    all_text_land = " ".join([item["text"] for item in ds_land])
    assert "Fanged Noumena" in all_text_land
    assert "Neo-China arrives from the future" in all_text_land
    assert "Meltdown: planetary china-syndrome" in all_text_land
    assert "Circuitries" in all_text_land

    ds_zizek = load_dataset("slavoj_zizek")
    # We added new content, so now there should be 6 items (4 original + 2 added)
    assert len(ds_zizek) == 6
    all_text_zizek = " ".join([item["text"] for item in ds_zizek])
    assert "Ideology" in all_text_zizek
    assert "start eating that trashcan" in all_text_zizek
    assert "Human Rights" in all_text_zizek
    assert "Today, everybody is talking about virtual reality" in all_text_zizek
    assert "Tolerance as an Ideological Category" in all_text_zizek

    ds_aurelius = load_dataset("marcus_aurelius")
    # We added new content, so now there should be 3 items (2 original + 1 added)
    assert len(ds_aurelius) == 3
    all_text_aurelius = " ".join([item["text"] for item in ds_aurelius])
    assert "Of my grandfather Verus" in all_text_aurelius

    print("Workflow test passed!")

if __name__ == "__main__":
    test_workflow()
