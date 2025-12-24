from socials_data.core.manager import PersonalityManager
from socials_data.core.processor import DataProcessor
import os

def clean_file(filepath, start_marker, end_marker, use_regex=False):
    with open(filepath, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    start_idx = 0
    end_idx = len(lines)

    # First pass: Strip standard Gutenberg headers/footers if markers aren't specific
    # (Actually, we can just do a direct search for the specific markers provided)

    for i, line in enumerate(lines):
        if start_marker in line:
            start_idx = i
            # If the marker is the book title, we might want to skip it or include it.
            # Usually we want to skip the line itself if it's just a marker,
            # but if it's "BOOK I", we might want to keep it.
            # For now, let's include the marker line unless it looks like a Gutenberg header.
            if "*** START" in line:
                start_idx = i + 1
            break

    for i, line in enumerate(lines):
        if end_marker in line:
            end_idx = i
            break

    # Refine start if we are still in metadata
    # (Optional logic could go here)

    cleaned_lines = lines[start_idx:end_idx]

    # Write back
    with open(filepath, 'w', encoding='utf-8') as f:
        f.writelines(cleaned_lines)
    print(f"Cleaned {filepath}")

def main():
    base_dir = os.path.join("socials_data", "personalities", "jean_jacques_rousseau", "raw")

    files_config = [
        {
            "file": "the_social_contract.txt",
            "start": "BOOK I",
            "end": "*** END OF THE PROJECT GUTENBERG EBOOK"
        },
        {
            "file": "confessions.txt",
            "start": "BOOK I.",
            "end": "*** END OF THE PROJECT GUTENBERG EBOOK"
        },
        {
            "file": "emile.txt",
            "start": "BOOK I",
            "end": "*** END OF THE PROJECT GUTENBERG EBOOK"
        },
        {
            "file": "discourse_on_inequality.txt",
            "start": "QUESTION PROPOSED BY THE ACADEMY OF DIJON",
            "end": "*** END OF THE PROJECT GUTENBERG EBOOK"
        }
    ]

    for config in files_config:
        filepath = os.path.join(base_dir, config["file"])
        if os.path.exists(filepath):
            clean_file(filepath, config["start"], config["end"])
        else:
            print(f"Warning: {filepath} not found.")

if __name__ == "__main__":
    main()
