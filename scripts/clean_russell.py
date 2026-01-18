import os
import re

def clean_gutenberg_text(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Patterns to identify start and end of Gutenberg text
    start_patterns = [
        r"\*\*\* START OF THE PROJECT GUTENBERG EBOOK .* \*\*\*",
        r"\*\*\* START OF THIS PROJECT GUTENBERG EBOOK .* \*\*\*",
        r"\*\*\* START OF PROJECT GUTENBERG EBOOK .* \*\*\*",
    ]
    end_patterns = [
        r"\*\*\* END OF THE PROJECT GUTENBERG EBOOK .* \*\*\*",
        r"\*\*\* END OF THIS PROJECT GUTENBERG EBOOK .* \*\*\*",
        r"\*\*\* END OF PROJECT GUTENBERG EBOOK .* \*\*\*",
        r"End of the Project Gutenberg EBook",
        r"End of Project Gutenberg's",
    ]

    start_idx = 0
    for pattern in start_patterns:
        match = re.search(pattern, content, re.IGNORECASE)
        if match:
            start_idx = match.end()
            break

    end_idx = len(content)
    for pattern in end_patterns:
        match = re.search(pattern, content, re.IGNORECASE)
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
