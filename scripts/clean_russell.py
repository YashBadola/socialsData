import os
import re

def clean_gutenberg_text(filepath):
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
    except UnicodeDecodeError:
        # Fallback for older encodings if utf-8 fails
        with open(filepath, 'r', encoding='latin-1') as f:
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
    for pattern in start_patterns:
        match = re.search(pattern, content)
        if match:
            start_idx = match.end()
            break

    end_idx = len(content)
    for pattern in end_patterns:
        match = re.search(pattern, content)
        if match:
            end_idx = match.start()
            break

    # Clean text
    text = content[start_idx:end_idx].strip()

    # Save back to file
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(text)
    print(f"Cleaned {filepath}")

base_dir = "socials_data/personalities/bertrand_russell/raw"

if not os.path.exists(base_dir):
    print(f"Directory not found: {base_dir}")
    exit(1)

for filename in os.listdir(base_dir):
    if filename.endswith(".txt"):
        filepath = os.path.join(base_dir, filename)
        clean_gutenberg_text(filepath)
