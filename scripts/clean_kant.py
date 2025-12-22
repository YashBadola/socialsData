import re
import sys
import os

def clean_kant_text(filepath):
    print(f"Cleaning {filepath}...")
    with open(filepath, 'r', encoding='utf-8') as f:
        text = f.read()

    # Find the start and end markers
    start_marker = "*** START OF THE PROJECT GUTENBERG EBOOK THE CRITIQUE OF PURE REASON ***"
    end_marker = "*** END OF THE PROJECT GUTENBERG EBOOK THE CRITIQUE OF PURE REASON ***"

    start_idx = text.find(start_marker)
    end_idx = text.find(end_marker)

    if start_idx == -1:
        print("Start marker not found! proceeding with caution (maybe manual check needed).")
        # Try a fallback or just start from 0, but ideally we warn.
        start_idx = 0
    else:
        start_idx += len(start_marker)

    if end_idx == -1:
        print("End marker not found! proceeding to end of file.")
        end_idx = len(text)

    content = text[start_idx:end_idx]

    # Remove the metadata illustration tag
    content = content.replace("[Illustration]", "")

    # Optional: Remove "Contents" table if it's just a list of chapters.
    # Looking at the head output:
    # Contents
    #  Preface...
    #  ...
    #  Introduction
    #
    # We might want to keep the content but maybe strip the TOC.
    # For now, I'll just strip leading/trailing whitespace.
    content = content.strip()

    # Write back to the same file
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

    print("Cleaned successfully.")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        clean_kant_text(sys.argv[1])
    else:
        print("Please provide a filepath.")
