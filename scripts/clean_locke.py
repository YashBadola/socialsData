import os

RAW_DIR = "socials_data/personalities/john_locke/raw"
FILES = [
    "second_treatise_of_government.txt",
    "essay_concerning_human_understanding_1.txt",
    "essay_concerning_human_understanding_2.txt"
]

def clean_file(filepath):
    print(f"Cleaning {filepath}...")
    with open(filepath, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    start_idx = 0
    end_idx = len(lines)

    # Markers for stripping Gutenberg headers/footers
    start_markers = [
        "*** START OF THE PROJECT GUTENBERG EBOOK",
        "*** START OF THIS PROJECT GUTENBERG EBOOK",
        "***START OF THE PROJECT GUTENBERG EBOOK"
    ]
    end_markers = [
        "*** END OF THE PROJECT GUTENBERG EBOOK",
        "*** END OF THIS PROJECT GUTENBERG EBOOK",
        "***END OF THE PROJECT GUTENBERG EBOOK"
    ]

    # Find start
    for i, line in enumerate(lines):
        for marker in start_markers:
            if marker in line:
                start_idx = i + 1
                break
        if start_idx > 0:
            break

    # Find end
    for i, line in enumerate(lines):
        if i < start_idx: continue
        for marker in end_markers:
            if marker in line:
                end_idx = i
                break
        if end_idx < len(lines):
            break

    content = lines[start_idx:end_idx]

    # Secondary cleaning for translator intros if needed
    # (Adjust based on inspection if specific intros persist)

    # Write back
    with open(filepath, 'w', encoding='utf-8') as f:
        f.writelines(content)
    print(f"Cleaned {filepath}")

if __name__ == "__main__":
    for filename in FILES:
        clean_file(os.path.join(RAW_DIR, filename))
