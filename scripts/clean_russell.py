import os
import re

def clean_gutenberg_text(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Patterns to identify start and end of Gutenberg text
    start_patterns = [
        r"\*\*\* START OF THE PROJECT GUTENBERG EBOOK .* \*\*\*",
        r"\*\*\* START OF THIS PROJECT GUTENBERG EBOOK .* \*\*\*",
    ]
    end_patterns = [
        r"\*\*\* END OF THE PROJECT GUTENBERG EBOOK .* \*\*\*",
        r"\*\*\* END OF THIS PROJECT GUTENBERG EBOOK .* \*\*\*",
    ]

    start_idx = 0
    found_start = False
    for pattern in start_patterns:
        match = re.search(pattern, content)
        if match:
            print(f"Matched start pattern in {os.path.basename(filepath)}: {match.group(0)}")
            start_idx = match.end()
            found_start = True
            break

    if not found_start:
        print(f"Warning: Start pattern not found in {filepath}")

    end_idx = len(content)
    found_end = False
    for pattern in end_patterns:
        match = re.search(pattern, content)
        if match:
            print(f"Matched end pattern in {os.path.basename(filepath)}: {match.group(0)}")
            end_idx = match.start()
            found_end = True
            break

    if not found_end:
        print(f"Warning: End pattern not found in {filepath}")

    # Clean text
    text = content[start_idx:end_idx].strip()

    # Save back to file
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(text)
    print(f"Cleaned {filepath}")

base_dir = "socials_data/personalities/bertrand_russell/raw"
files = [
    "problems_of_philosophy.txt",
    "analysis_of_mind.txt",
    "mysticism_and_logic.txt"
]

for filename in files:
    filepath = os.path.join(base_dir, filename)
    if os.path.exists(filepath):
        clean_gutenberg_text(filepath)
    else:
        print(f"File not found: {filepath}")
