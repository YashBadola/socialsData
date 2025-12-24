import os
import re

def clean_file(filepath, start_markers, end_markers):
    with open(filepath, 'r', encoding='utf-8-sig') as f:
        content = f.read()

    start_idx = 0
    # Search for start markers in order
    for marker in start_markers:
        idx = content.find(marker)
        if idx != -1:
            start_idx = idx
            break

    if start_idx == 0:
        print(f"Warning: No start marker found for {filepath}")

    end_idx = len(content)
    # Search for end markers. We want the EARLIEST occurrence of any end marker after start_idx.
    # So we iterate and find the min index.
    found_end = False
    for marker in end_markers:
        idx = content.find(marker, start_idx)
        if idx != -1:
            if idx < end_idx:
                end_idx = idx
            found_end = True

    if not found_end:
        print(f"Warning: No end marker found for {filepath}")

    cleaned_content = content[start_idx:end_idx].strip()

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(cleaned_content)
    print(f"Cleaned {filepath}")

def main():
    base_dir = "socials_data/personalities/voltaire/raw"

    # Candide
    clean_file(
        os.path.join(base_dir, "candide.txt"),
        start_markers=["HOW CANDIDE WAS BROUGHT UP"],
        end_markers=["*** END OF THE PROJECT GUTENBERG EBOOK", "End of the Project Gutenberg EBook"]
    )

    # Zadig
    clean_file(
        os.path.join(base_dir, "zadig.txt"),
        start_markers=["SULTANA _SHERAA_,"],
        end_markers=["*** END OF THE PROJECT GUTENBERG EBOOK", "End of the Project Gutenberg EBook"]
    )

    # Micromegas
    clean_file(
        os.path.join(base_dir, "micromegas.txt"),
        start_markers=["CHAPTER I."],
        end_markers=[
            "End of Project Gutenberg's Romans",
            "*** END OF THE PROJECT GUTENBERG EBOOK",
            "End of the Project Gutenberg EBook"
        ]
    )

    # Letters on England
    clean_file(
        os.path.join(base_dir, "letters_on_england.txt"),
        start_markers=["LETTER I.--ON THE QUAKERS"],
        end_markers=["*** END OF THE PROJECT GUTENBERG EBOOK", "End of the Project Gutenberg EBook"]
    )

if __name__ == "__main__":
    main()
