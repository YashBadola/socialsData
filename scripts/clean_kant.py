import os
import re

def clean_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Generic Project Gutenberg header/footer cleaner
    # Look for "START OF THE PROJECT GUTENBERG EBOOK" and "END OF THE PROJECT GUTENBERG EBOOK"

    start_markers = [
        r"\*\*\* START OF THE PROJECT GUTENBERG EBOOK .* \*\*\*",
        r"\*\*\* START OF THIS PROJECT GUTENBERG EBOOK .* \*\*\*",
    ]

    end_markers = [
        r"\*\*\* END OF THE PROJECT GUTENBERG EBOOK .* \*\*\*",
        r"\*\*\* END OF THIS PROJECT GUTENBERG EBOOK .* \*\*\*",
    ]

    start_idx = 0
    for marker in start_markers:
        match = re.search(marker, content, re.IGNORECASE)
        if match:
            start_idx = match.end()
            break

    end_idx = len(content)
    for marker in end_markers:
        match = re.search(marker, content, re.IGNORECASE)
        if match:
            end_idx = match.start()
            break

    if start_idx == 0:
        print(f"Warning: No start marker found in {filepath}")

    if end_idx == len(content):
        print(f"Warning: No end marker found in {filepath}")

    cleaned_content = content[start_idx:end_idx].strip()

    # Also remove common legal disclaimers if they appear before the marker
    # (Sometimes they do)

    # Save back
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(cleaned_content)
    print(f"Cleaned {filepath}")

base_path = "socials_data/personalities/immanuel_kant/raw"
files = [
    os.path.join(base_path, "critique_pure_reason.txt"),
    os.path.join(base_path, "metaphysic_morals.txt")
]

for f in files:
    clean_file(f)
