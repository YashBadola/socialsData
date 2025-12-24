import os
import re

def clean_file(filepath):
    with open(filepath, 'r', encoding='utf-8-sig') as f:
        content = f.read()

    # Define markers
    start_marker = "*** START OF THE PROJECT GUTENBERG EBOOK SELECTIONS FROM THE WRITINGS OF KIERKEGAARD ***"
    end_marker = "*** END OF THE PROJECT GUTENBERG EBOOK SELECTIONS FROM THE WRITINGS OF KIERKEGAARD ***"

    # Find start and end
    start_idx = content.find(start_marker)
    end_idx = content.find(end_marker)

    if start_idx == -1 or end_idx == -1:
        print(f"Markers not found in {filepath}")
        return

    # Extract content
    content = content[start_idx + len(start_marker):end_idx]

    # Further clean up preamble if needed
    # The file has "UNIVERSITY OF TEXAS BULLETIN..." then "INTRODUCTION I"
    # Let's skip to the actual INTRODUCTION I if possible, or just keep it all after the marker.
    # Looking at the head output:
    # It has a bunch of title page stuff, then "CONTENTS", then "INTRODUCTION I"
    # Let's try to find "INTRODUCTION I" to skip the front matter if we want, or just keep it.
    # The prompt usually wants the text.
    # But "INTRODUCTION I" seems to be part of the text (Intro by Hollander).
    # "DIAPSALMATA" starts later.
    # The memory says "first isolating content between the standard Gutenberg headers and footers, then refining the start index by searching for a specific internal marker (e.g., the first line of the actual text) to remove translator introductions."
    # Hollander's introduction is valuable context but maybe we want Kierkegaard's voice.
    # However, this is "Selections", so the intro might be by the editor.
    # "Creditable as have been the contributions of Scandinavia... it has produced but one thinker..." - That's Hollander.
    # The actual text starts with "DIAPSALMATA".
    # But wait, the table of contents lists "INTRODUCTION".
    # Let's look for "DIAPSALMATA" to start the actual Kierkegaard text?
    # Or maybe we should include the introduction?
    # Usually we want the philosopher's words.
    # Let's check where "DIAPSALMATA" starts.

    diapsalmata_marker = "DIAPSALMATA"
    # There is a "CONTENTS" list which contains "DIAPSALMATA".
    # Then there is "INTRODUCTION I".
    # Then presumably "DIAPSALMATA" again as a header.

    # Let's keep it simple for now and just strip the Gutenberg headers.
    # If the introduction is by the translator, it might be better to skip it, but sometimes it's hard to separate cleanly without losing text if the structure is complex.
    # Let's look for the first occurrence of "DIAPSALMATA" after "INTRODUCTION".

    # Actually, looking at the file content, "INTRODUCTION I" is definitely the translator.
    # "DIAPSALMATA" follows it.

    # Let's try to find the start of "DIAPSALMATA" section.
    # It might appear in TOC first.
    # The TOC has:
    # CONTENTS
    # INTRODUCTION.
    # DIAPSALMATA.

    # So the second "DIAPSALMATA" should be the start.
    # Or we can look for "Ad se ipsum" which is often the subtitle or just the text start.

    # Let's stick to just stripping Gutenberg headers for now to be safe, unless I can confirm the exact start line.
    # I'll just strip whitespace.

    content = content.strip()

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"Cleaned {filepath}")

if __name__ == "__main__":
    clean_file("socials_data/personalities/soren_kierkegaard/raw/selections.txt")
