import os
import re

def clean_kant():
    raw_path = 'socials_data/personalities/immanuel_kant/raw/critique_of_pure_reason.txt'

    with open(raw_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Find start and end markers
    start_marker = "*** START OF THE PROJECT GUTENBERG EBOOK THE CRITIQUE OF PURE REASON ***"
    end_marker = "*** END OF THE PROJECT GUTENBERG EBOOK THE CRITIQUE OF PURE REASON ***"

    start_index = content.find(start_marker)
    end_index = content.find(end_marker)

    if start_index == -1 or end_index == -1:
        print("Markers not found!")
        return

    # Extract the text between markers
    cleaned_text = content[start_index + len(start_marker):end_index].strip()

    # Optionally remove some extra preamble if needed.
    # Checking the file via head/tail is useful, but the standard cut is usually decent.
    # Often there is a "Produced by..." line right after the marker.

    # Write back
    with open(raw_path, 'w', encoding='utf-8') as f:
        f.write(cleaned_text)

    print(f"Cleaned {raw_path}")

if __name__ == "__main__":
    clean_kant()
