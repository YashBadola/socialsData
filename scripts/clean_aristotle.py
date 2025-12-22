import os
import re

def clean_gutenberg_text(text):
    """
    Removes Project Gutenberg headers and footers.
    """
    # Patterns for start and end of Gutenberg texts
    start_patterns = [
        r"\*\*\* START OF THE PROJECT GUTENBERG EBOOK .* \*\*\*",
        r"\*\*\* START OF THIS PROJECT GUTENBERG EBOOK .* \*\*\*",
        r"\*\*\*START OF THE PROJECT GUTENBERG EBOOK .*\*\*\*",
        r"\*\*\*START OF THIS PROJECT GUTENBERG EBOOK .*\*\*\*",
    ]
    end_patterns = [
        r"\*\*\* END OF THE PROJECT GUTENBERG EBOOK .* \*\*\*",
        r"\*\*\* END OF THIS PROJECT GUTENBERG EBOOK .* \*\*\*",
        r"\*\*\*END OF THE PROJECT GUTENBERG EBOOK .*\*\*\*",
        r"\*\*\*END OF THIS PROJECT GUTENBERG EBOOK .*\*\*\*",
    ]

    start_idx = 0
    end_idx = len(text)

    for pattern in start_patterns:
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            start_idx = max(start_idx, match.end())

    for pattern in end_patterns:
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            end_idx = min(end_idx, match.start())

    # Add a buffer for any intro text that often follows the header
    # But usually, we just want to strip the license stuff.
    # Often there is a "Produced by..." line after the start header.

    clean_text = text[start_idx:end_idx].strip()

    return clean_text

def clean_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        text = f.read()

    cleaned = clean_gutenberg_text(text)

    # Specific cleaning for Aristotle texts if needed
    # For now, just Gutenberg cleaning is a good start.

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(cleaned)
    print(f"Cleaned {filepath}")

if __name__ == "__main__":
    base_dir = "socials_data/personalities/aristotle/raw"
    files = [
        "nicomachean_ethics.txt",
        "politics.txt",
        "poetics.txt",
        "de_anima.txt"
    ]

    for filename in files:
        filepath = os.path.join(base_dir, filename)
        if os.path.exists(filepath):
            clean_file(filepath)
        else:
            print(f"File not found: {filepath}")
