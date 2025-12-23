import os

PERSONALITY_ID = "william_james"
RAW_DIR = os.path.join("socials_data", "personalities", PERSONALITY_ID, "raw")

# Filename -> (Start Marker, End Marker)
# If Start Marker is a string, we look for it.
# If End Marker is a string, we look for it.
FILES_CONFIG = {
    "pragmatism.txt": (
        "*** START OF THE PROJECT GUTENBERG EBOOK PRAGMATISM: A NEW NAME FOR SOME OLD WAYS OF THINKING ***",
        "*** END OF THE PROJECT GUTENBERG EBOOK PRAGMATISM: A NEW NAME FOR SOME OLD WAYS OF THINKING ***"
    ),
    "varieties_of_religious_experience.txt": (
        "*** START OF THE PROJECT GUTENBERG EBOOK THE VARIETIES OF RELIGIOUS EXPERIENCE: A STUDY IN HUMAN NATURE ***",
        "*** END OF THE PROJECT GUTENBERG EBOOK THE VARIETIES OF RELIGIOUS EXPERIENCE: A STUDY IN HUMAN NATURE ***"
    ),
    "will_to_believe.txt": (
        "*** START OF THE PROJECT GUTENBERG EBOOK THE WILL TO BELIEVE, AND OTHER ESSAYS IN POPULAR PHILOSOPHY ***",
        "*** END OF THE PROJECT GUTENBERG EBOOK THE WILL TO BELIEVE, AND OTHER ESSAYS IN POPULAR PHILOSOPHY ***"
    )
}

def clean_file(filename, markers):
    filepath = os.path.join(RAW_DIR, filename)
    if not os.path.exists(filepath):
        print(f"File not found: {filepath}")
        return

    with open(filepath, 'r', encoding='utf-8-sig') as f:
        lines = f.readlines()

    start_marker, end_marker = markers
    start_idx = -1
    end_idx = -1

    for i, line in enumerate(lines):
        if start_marker in line:
            start_idx = i
        if end_marker in line:
            end_idx = i
            # If we found both, break? Wait, sometimes end marker appears early? No.
            # Usually end marker is at the end.

    if start_idx == -1:
        print(f"Start marker not found in {filename}")
        return
    if end_idx == -1:
        print(f"End marker not found in {filename}")
        return

    # Extract content, skipping the marker lines themselves
    # And maybe some whitespace around it
    content_lines = lines[start_idx + 1 : end_idx]

    # Strip leading/trailing empty lines
    while content_lines and not content_lines[0].strip():
        content_lines.pop(0)
    while content_lines and not content_lines[-1].strip():
        content_lines.pop()

    new_content = "".join(content_lines)

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(new_content)

    print(f"Cleaned {filename}")

def main():
    for filename, markers in FILES_CONFIG.items():
        clean_file(filename, markers)

if __name__ == "__main__":
    main()
