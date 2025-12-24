import os
import re

def clean_file(filepath, start_marker, end_marker=None):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Find start
    if isinstance(start_marker, str):
        start_marker = [start_marker]

    start_idx = -1
    for marker in start_marker:
        idx = content.find(marker)
        if idx != -1:
            start_idx = idx
            break

    if start_idx == -1:
        print(f"WARNING: Start marker not found in {filepath}. Content start might be incorrect.")
        # Fallback to standard Gutenberg start if specific marker fails
        match = re.search(r"\*\*\* START OF THE PROJECT GUTENBERG EBOOK .* \*\*\*", content)
        if match:
             start_idx = match.end()
        else:
             start_idx = 0

    # Find end
    end_idx = -1
    if end_marker:
        end_idx = content.find(end_marker)

    if end_idx == -1:
        # We need to catch "End of the Project Gutenberg EBook..." AND "End of Project Gutenberg's..."
        # Regex is safer.
        # Variations seen:
        # "*** END OF THE PROJECT GUTENBERG EBOOK..."
        # "End of Project Gutenberg's..."
        # "End of the Project Gutenberg EBook..."

        # We will look for the first occurrence of any of these patterns.
        patterns = [
            r"\*\*\* END OF THE PROJECT GUTENBERG EBOOK",
            r"End of Project Gutenberg's",
            r"End of the Project Gutenberg",
        ]

        candidates = []
        for pat in patterns:
            match = re.search(pat, content, re.IGNORECASE)
            if match:
                candidates.append(match.start())

        if candidates:
            end_idx = min(candidates)
        else:
            end_idx = len(content)

    text = content[start_idx:end_idx].strip()

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(text)
    print(f"Cleaned {filepath}")

base_dir = "socials_data/personalities/ralph_waldo_emerson/raw"

# Define markers for each file
files_config = [
    {
        "filename": "essays_first_series.txt",
        "start": "HISTORY",
    },
    {
        "filename": "essays_second_series.txt",
        "start": "I. THE POET.",
    },
    {
        "filename": "nature.txt",
        "start": "INTRODUCTION.",
    },
    {
        "filename": "representative_men.txt",
        "start": "I. USES OF GREAT MEN.",
    },
    {
        "filename": "conduct_of_life.txt",
        "start": "FATE.",
    }
]

for config in files_config:
    filepath = os.path.join(base_dir, config["filename"])
    if os.path.exists(filepath):
        clean_file(filepath, config["start"])
    else:
        print(f"File not found: {filepath}")
