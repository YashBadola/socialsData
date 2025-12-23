import os
import re

def clean_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Find Start
    start_match = re.search(r'\*\*\* START OF THE PROJECT GUTENBERG EBOOK .* \*\*\*', content)
    if start_match:
        content = content[start_match.end():]
    else:
        print(f"Warning: Start marker not found in {filepath}")

    # Find End
    end_match = re.search(r'\*\*\* END OF THE PROJECT GUTENBERG EBOOK .* \*\*\*', content)
    if end_match:
        content = content[:end_match.start()]
    else:
        print(f"Warning: End marker not found in {filepath}")

    # Strip leading/trailing whitespace
    content = content.strip()

    # Write back
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"Cleaned {filepath}")

if __name__ == "__main__":
    files = [
        "socials_data/personalities/david_hume/raw/treatise_human_nature.txt",
        "socials_data/personalities/david_hume/raw/enquiry_human_understanding.txt"
    ]
    for f in files:
        if os.path.exists(f):
            clean_file(f)
        else:
            print(f"File not found: {f}")
