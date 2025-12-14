from socials_data import load_dataset
import pytest

def test_workflow():
    # Verify we can load the data we just created
    ds_land = load_dataset("nick_land")
    assert len(ds_land) == 2
    assert "Fanged Noumena" in ds_land[0]["text"]
    assert "Neo-China arrives from the future" in ds_land[1]["text"]

    ds_zizek = load_dataset("slavoj_zizek")
    assert len(ds_zizek) == 2
    assert "Ideology" in ds_zizek[0]["text"]
    assert "start eating that trashcan" in ds_zizek[1]["text"]

    print("Workflow test passed!")

if __name__ == "__main__":
    test_workflow()
