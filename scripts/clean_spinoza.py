import sys
import re

def clean_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Find the start and end of the Project Gutenberg text
    # Observed from 'head' command: "*** START OF THE PROJECT GUTENBERG EBOOK ETHICS ***"
    start_marker = "*** START OF THE PROJECT GUTENBERG EBOOK ETHICS ***"

    # Guessing the end marker based on common patterns, but I'll search for "END OF THE PROJECT GUTENBERG"
    # Or I can just look for the last meaningful text.
    # The tail output shows "Professor Michael S. Hart...", so I should look for the end marker before that.
    # Usually it is "*** END OF THE PROJECT GUTENBERG EBOOK ETHICS ***" or similar.

    start_idx = content.find(start_marker)

    if start_idx != -1:
        content = content[start_idx + len(start_marker):]
    else:
        print("Warning: Start marker not found.")

    # Try to find end marker
    end_marker = "*** END OF THE PROJECT GUTENBERG EBOOK ETHICS ***"
    end_idx = content.find(end_marker)

    if end_idx != -1:
        content = content[:end_idx]
    else:
        # Fallback end marker search
        end_idx = content.find("*** END OF THE PROJECT GUTENBERG")
        if end_idx != -1:
            content = content[:end_idx]

    # Additional cleanup
    content = content.strip()

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

    print(f"Cleaned {filepath}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python clean_spinoza.py <filepath>")
        sys.exit(1)

    clean_file(sys.argv[1])
