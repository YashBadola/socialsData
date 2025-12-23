import os
import re

def clean_file(filepath):
    with open(filepath, 'r', encoding='utf-8-sig') as f:
        content = f.read()

    # Identify Gutenberg header end
    # Typically: "*** START OF THE PROJECT GUTENBERG EBOOK ... ***"
    start_match = re.search(r'\*\*\* START OF (THE|THIS) PROJECT GUTENBERG EBOOK .* \*\*\*', content)

    start_index = 0
    if start_match:
        start_index = start_match.end()

    # Identify Gutenberg footer start
    # Typically: "*** END OF THE PROJECT GUTENBERG EBOOK ... ***"
    end_match = re.search(r'\*\*\* END OF (THE|THIS) PROJECT GUTENBERG EBOOK .* \*\*\*', content)

    end_index = len(content)
    if end_match:
        end_index = end_match.start()

    text = content[start_index:end_index].strip()

    # Second pass: Look for specific markers if possible or generic removal of preamble
    # For Plato's Republic, it often starts with "The Republic" or "INTRODUCTION" or "BOOK I".
    # Since specific markers vary, we will stick to stripping the Gutenberg wrappers which is the primary requirement.
    # However, to improve quality, let's try to remove the license text if it lingers.

    # Check for "Produced by" lines which often appear after the start marker
    # But usually start_match covers it.

    # Save back
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(text)

    print(f"Cleaned {filepath}")

if __name__ == "__main__":
    base_dir = "socials_data/personalities/plato/raw"
    files = ["the_republic.txt", "symposium.txt", "apology.txt"]
    for file in files:
        filepath = os.path.join(base_dir, file)
        if os.path.exists(filepath):
            clean_file(filepath)
        else:
            print(f"File not found: {filepath}")
