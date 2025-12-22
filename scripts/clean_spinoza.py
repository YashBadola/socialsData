import os
import re

def clean_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Generic Project Gutenberg header/footer removal
    # Find start
    start_match = re.search(r'\*\*\* START OF (THE|THIS) PROJECT GUTENBERG EBOOK .* \*\*\*', content, re.IGNORECASE)
    if start_match:
        content = content[start_match.end():]

    # Find end
    end_match = re.search(r'\*\*\* END OF (THE|THIS) PROJECT GUTENBERG EBOOK .* \*\*\*', content, re.IGNORECASE)
    if end_match:
        content = content[:end_match.start()]

    # Clean up excessive whitespace
    content = content.strip()

    # Save back
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"Cleaned {filepath}")

if __name__ == "__main__":
    base_dir = "socials_data/personalities/baruch_spinoza/raw"
    for filename in os.listdir(base_dir):
        if filename.endswith(".txt"):
            clean_file(os.path.join(base_dir, filename))
