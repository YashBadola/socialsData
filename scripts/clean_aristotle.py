import os
import re

def clean_file(filepath, start_markers, end_markers):
    with open(filepath, 'r', encoding='utf-8-sig') as f:
        content = f.read()

    start_idx = 0
    found_start = False

    # Try markers in order
    for marker in start_markers:
        idx = content.find(marker)
        if idx != -1:
            # If marker is "Part 1" or similar content start, we want to KEEP it, so start_idx = idx
            # If marker is a header we want to skip (like "INTRODUCTION"), we want start_idx = idx + len(marker)
            # But here we are looking for the START OF CONTENT.
            # So if we find "Part 1", we want the text to start AT "Part 1".
            # The previous script did `idx + len(marker)`, which skips the marker.
            # Let's adjust logic: if the marker is a "Title" or "Header" to be stripped, we skip it.
            # If it's the first line of text, we want to include it.
            # For simplicity, let's assume markers are unique phrases at the START of the text we want to KEEP,
            # OR unique phrases at the END of the junk we want to SKIP.

            # Case 1: Marker is the start of the text we want (e.g. "I propose to treat").
            # We should set start_idx = idx.

            # Case 2: Marker is the end of the junk (e.g. "*** START OF THIS PROJECT GUTENBERG EBOOK... ***").
            # We should set start_idx = idx + len(marker).

            # Current config uses markers like "Part 1" which are part of the text.
            # So let's change the logic to: found marker -> that's the start.

            # EXCEPT if the marker is explicitly a "skip" marker.
            # Let's just use the start of the actual text as the marker and include it.
            start_idx = idx
            print(f"Found content start at '{marker}' in {filepath}")
            found_start = True
            break

    if not found_start:
         print(f"WARNING: No content start marker found for {filepath}")

    end_idx = len(content)
    found_end = False
    for marker in end_markers:
        idx = content.rfind(marker)
        if idx != -1:
            end_idx = idx
            print(f"Found end marker '{marker}' in {filepath}")
            found_end = True
            break

    if not found_end:
        print(f"WARNING: No end marker found for {filepath}")

    cleaned_content = content[start_idx:end_idx].strip()

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(cleaned_content)
    print(f"Cleaned {filepath} (Size: {len(cleaned_content)})")

base_dir = "socials_data/personalities/aristotle/raw"

# Config for each file
files_config = [
    {
        "file": "nicomachean_ethics.txt",
        # Starts with "BOOK I"
        "start_markers": ["BOOK I"],
        "end_markers": ["END OF THE PROJECT GUTENBERG EBOOK", "*** END OF THE PROJECT", "End of the Project Gutenberg"]
    },
    {
        "file": "politics.txt",
        # Starts with "A TREATISE ON GOVERNMENT" -> "BOOK I"
        "start_markers": ["BOOK I"],
        "end_markers": ["END OF THE PROJECT GUTENBERG EBOOK", "*** END OF THE PROJECT", "End of the Project Gutenberg"]
    },
    {
        "file": "poetics.txt",
        # Starts with "I propose to treat of Poetry"
        "start_markers": ["I propose to treat of Poetry"],
        "end_markers": ["END OF THE PROJECT GUTENBERG EBOOK", "*** END OF THE PROJECT", "End of the Project Gutenberg"]
    },
    {
        "file": "categories.txt",
        # Starts with "Part 1"
        "start_markers": ["Part 1"],
        "end_markers": ["END OF THE PROJECT GUTENBERG EBOOK", "*** END OF THE PROJECT", "End of the Project Gutenberg"]
    }
]

for config in files_config:
    filepath = os.path.join(base_dir, config["file"])
    clean_file(filepath, config["start_markers"], config["end_markers"])
