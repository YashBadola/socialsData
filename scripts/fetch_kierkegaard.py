import requests
from pathlib import Path
import re

URL = "https://www.gutenberg.org/cache/epub/60333/pg60333.txt"
OUTPUT_DIR = Path("socials_data/personalities/soren_kierkegaard/raw")

def main():
    print(f"Downloading from {URL}...")
    response = requests.get(URL)
    response.raise_for_status()
    text = response.text
    print(f"Downloaded {len(text)} characters.")

    # Find the start of the content (skip TOC)
    start_intro_marker = "INTRODUCTION I"
    start_intro = text.find(start_intro_marker)
    if start_intro == -1:
        print("Could not find start marker 'INTRODUCTION I'. Aborting.")
        return

    print(f"Found Introduction at index {start_intro}")

    work_titles = [
        ("DIAPSALMATA", "diapsalmata.txt"),
        ("IN VINO VERITAS (THE BANQUET)", "in_vino_veritas.txt"),
        ("FEAR AND TREMBLING", "fear_and_trembling.txt"),
        ("PREPARATION FOR A CHRISTIAN LIFE", "preparation_for_christian_life.txt"),
        ("THE PRESENT MOMENT", "the_present_moment.txt")
    ]

    current_pos = start_intro
    positions = []

    for title, filename in work_titles:
        # Find title after current_pos
        pos = text.find(title, current_pos)
        if pos == -1:
            # Try fuzzy match or look for variations if exact match fails
            # For "THE PRESENT MOMENT", it might be "THE PRESENT MOMENT[1]" or similar
            print(f"Warning: Could not find exact match for '{title}'. Trying alternatives...")
            if title == "DIAPSALMATA":
                 pos = text.find("DIAPSALMATA[1]", current_pos)
            elif title == "THE PRESENT MOMENT":
                 pos = text.find("THE PRESENT MOMENT[1]", current_pos)

            if pos == -1:
                print(f"Error: Could not find '{title}' or alternatives.")
                continue

        print(f"Found '{title}' at index {pos}")
        positions.append((pos, title, filename))
        current_pos = pos + len(title)

    # End marker
    end_marker = "*** END OF THE PROJECT GUTENBERG EBOOK"
    end_pos = text.find(end_marker)
    if end_pos == -1:
        end_pos = len(text)

    positions.append((end_pos, "END", "END"))

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    # Save files
    for i in range(len(positions) - 1):
        start_idx = positions[i][0]
        end_idx = positions[i+1][0]
        title = positions[i][1]
        filename = positions[i][2]

        content = text[start_idx:end_idx].strip()

        output_path = OUTPUT_DIR / filename
        print(f"Writing {filename} ({len(content)} chars)...")
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(content)

if __name__ == "__main__":
    main()
