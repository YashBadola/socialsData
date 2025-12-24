import os

PERSONALITY_ID = "plato"
RAW_DIR = f"socials_data/personalities/{PERSONALITY_ID}/raw"

FILES = [
    "the_republic.txt",
    "symposium.txt",
    "apology.txt",
    "phaedo.txt",
]

def clean_file(filename):
    filepath = os.path.join(RAW_DIR, filename)
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Generic markers
    start_markers = [
        "*** START OF THE PROJECT GUTENBERG EBOOK",
        "*** START OF THIS PROJECT GUTENBERG EBOOK"
    ]
    end_markers = [
        "*** END OF THE PROJECT GUTENBERG EBOOK",
        "*** END OF THIS PROJECT GUTENBERG EBOOK"
    ]

    start_idx = -1
    for marker in start_markers:
        idx = content.find(marker)
        if idx != -1:
            # Move past the marker line
            end_of_marker_line = content.find('\n', idx)
            if end_of_marker_line != -1:
                start_idx = end_of_marker_line + 1
            else:
                 start_idx = idx + len(marker)
            break

    end_idx = -1
    for marker in end_markers:
        idx = content.find(marker)
        if idx != -1:
            end_idx = idx
            break

    if start_idx != -1 and end_idx != -1:
        # Strip potential introduction/metadata often found after start marker
        # But for now, let's just get the main block.
        # Actually, looking at the head output, there is often a title page or translator note.
        # Ideally we'd skip that, but it varies.
        # E.g. Republic: "THE REPUBLIC\nBy Plato\n..."
        # E.g. Symposium: "SYMPOSIUM\nBy Plato\n..."

        cleaned_content = content[start_idx:end_idx].strip()

        # Simple heuristic to skip title/translator repetition if present at very start
        # This is a bit risky if we aren't careful, but let's try to remove lines until we hit meaningful text?
        # No, that's hard.
        # For now, just removing the Gutenberg headers is a huge win.

        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(cleaned_content)
        print(f"Cleaned {filename}")
    else:
        print(f"Warning: Could not find markers in {filename}")

if __name__ == "__main__":
    for filename in FILES:
        clean_file(filename)
