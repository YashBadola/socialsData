import os
import re

def clean_gutenberg_text(filepath):
    print(f"Cleaning {filepath}...")
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Patterns to identify start and end of Gutenberg text
    # Note: These patterns are case-sensitive in the original script but might need to be looser.
    # Gutenberg headers vary.
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

    # If no match, try case insensitive search or generic marker
    if start_idx == 0:
         match = re.search(r"\*\*\* START OF .* PROJECT GUTENBERG .*", content, re.IGNORECASE)
         if match:
             start_idx = match.end()


    end_idx = len(content)
    for pattern in end_patterns:
        match = re.search(pattern, content)
        if match:
            end_idx = match.start()
            break

    if end_idx == len(content):
         match = re.search(r"\*\*\* END OF .* PROJECT GUTENBERG .*", content, re.IGNORECASE)
         if match:
             end_idx = match.start()

    # Clean text
    text = content[start_idx:end_idx].strip()

    # Save back to file
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(text)
    print(f"Cleaned {filepath}. New size: {len(text)} chars.")

base_dir = "socials_data/personalities/jean_jacques_rousseau/raw"
files = [
    "the_social_contract.txt",
    "confessions.txt"
]

for filename in files:
    filepath = os.path.join(base_dir, filename)
    if os.path.exists(filepath):
        clean_gutenberg_text(filepath)
    else:
        print(f"File not found: {filepath}")
