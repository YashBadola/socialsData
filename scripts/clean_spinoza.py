import os
import re

def clean_text(text):
    # Remove Gutenberg header
    # Often starts with *** START OF THIS PROJECT GUTENBERG EBOOK ... *** or *** START OF THE PROJECT GUTENBERG EBOOK ... ***
    start_pattern = re.compile(r'\*\*\* START OF (THE|THIS) PROJECT GUTENBERG EBOOK .*? \*\*\*', re.IGNORECASE)
    end_pattern = re.compile(r'\*\*\* END OF (THE|THIS) PROJECT GUTENBERG EBOOK .*? \*\*\*', re.IGNORECASE)

    start_match = start_pattern.search(text)
    end_match = end_pattern.search(text)

    start_idx = 0
    end_idx = len(text)

    if start_match:
        start_idx = start_match.end()

    if end_match:
        end_idx = end_match.start()

    cleaned = text[start_idx:end_idx].strip()

    # Also remove the "Produced by..." lines that often follow the header
    cleaned = re.sub(r'^Produced by .*?$', '', cleaned, flags=re.MULTILINE)

    return cleaned

def clean_file(filepath):
    print(f"Cleaning {filepath}...")
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    cleaned = clean_text(content)

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(cleaned)
    print(f"Cleaned {filepath}.")

if __name__ == "__main__":
    base_dir = "socials_data/personalities/baruch_spinoza/raw"
    files = ["ethics.txt", "theologico_political_treatise.txt"]

    for filename in files:
        filepath = os.path.join(base_dir, filename)
        if os.path.exists(filepath):
            clean_file(filepath)
        else:
            print(f"File not found: {filepath}")
